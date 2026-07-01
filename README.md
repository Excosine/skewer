# 签子计数 — 竹签识别计价系统

基于 YOLO 视觉识别与 Vue3 的餐饮签子自动计数计价系统，含管理后台与服务员移动端。

```
签子计数/
├── backend/     Python FastAPI 服务端    (port 8000)
├── admin/       Vue3 管理后台           (port 3000)
├── waiter/      Vue3 服务员移动端        (port 5173)
├── install.py   一键安装依赖
├── start.py     一键启动全部服务
└── logs/        运行日志（各服务独立文件）
```

---

## 技术架构

```
┌──────────┐  ┌──────────┐
│  admin   │  │  waiter  │   Vue3 + Vite
│  :3000   │  │  :5173   │   Element Plus / Tailwind CSS
└────┬─────┘  └────┬─────┘
     │  /api         │  /api
     ▼               ▼
┌──────────────────────────┐
│       FastAPI :8000      │   Python
│  JWT + bcrypt + SQLite   │   uv 包管理
└──────────┬───────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
┌───────┐   ┌──────────┐
│SQLite │   │  YOLO    │    YOLOv8 检测模型
│ WAL   │   │ 模型推理  │    竹签头圆检测
└───────┘   └──────────┘
```

---

## 快速开始

```bash
# 1. 安装依赖
python install.py

# 2. 启动全部服务
python start.py

# 或选择性启动
python start.py --backend
python start.py --admin --waiter
```

启动后访问：
- 管理后台：http://localhost:3000  账号 `admin / 123456`
- 服务员端：http://localhost:5173  账号 `waiter01 / 123456`
- API 文档：http://localhost:8000/docs

---

## 技术重点

### 1. 基于 JWT 的认证体系

- **bcrypt** 密码哈希，即使数据库泄露密码也不可逆
- JWT Token 24 小时过期，HS256 签名
- 前端 Axios 拦截器 / Pinia Store 统一管理 token，401 自动跳登录
- **图形验证码**：后端 Pillow 生成 PNG，内存缓存 5 分钟过期，一次性使用，大小写不敏感比对
- 管理员/服务员双角色 guard，`_deps.py` 提供 `current_user` 和 `admin_only` 依赖注入

### 2. 基于 YOLO 的竹签自动计数

**推理流程**：服务员拍照上传 → 后端写临时文件 → 加载 YOLO 模型 → 推理检测 → 返回竹签数量 + 置信度 → 自动更新订单 → 清理临时文件

**核心实现** (`detector/detector.py`)：
- 使用 Ultralytics YOLO（YOLOv8+）目标检测模型，权重文件 `weights/model.pt`
- 模型将竹签截面检测为矩形框（`xywh`），取长边半径作为输出 (`r = max(w, h) / 2`)
- 每个检测结果包含：`{cx, cy, r, score}` — 圆心坐标、半径、置信度
- 置信度阈值默认 0.25，可过滤低质量误检
- 自动检测设备：有 CUDA 用 GPU，无则回退 CPU

**性能优化**：
- **Lazy Singleton 模式**：`services/detection.py` 模块级单例 `_get_detector()`，首次推理加载模型（加载耗时的 `model.pt`），后续请求复用同一个模型实例，避免每次扫描都重复加载
- 临时文件 `finally` 块确保删除，不残留磁盘

**可视化调试** (`StickDetector.draw()`)：
```python
detector.draw("input.jpg", circles, "output.png")
```
输出标注图：绿色圆框标注检测区域、红色中心点、颜色深浅反映置信度高低

**CLI 独立调试** (`python -m detector.cli`)：
```bash
python -m detector.cli photo.jpg                # 输出 count
python -m detector.cli photo.jpg --json          # 输出 JSON（含每个圆的坐标和分数）
python -m detector.cli photo.jpg --debug         # 保存标注图
python -m detector.cli photo.jpg --conf 0.5      # 自定义阈值
```
无需启动服务，可独立验证模型效果。

### 3. 数据库设计

BCNF 范式，9 张表。详见 `backend/schema.sql`。

| 表 | 核心字段 | 说明 |
|----|----------|------|
| roles | id, name | admin / waiter |
| users | username, password_hash (**bcrypt**), role_id, status | 用户认证 |
| table_zones | name, surcharge, sort_order | 区域（大厅+0 / 包间+10 / 露台+5） |
| tables | zone_id, table_code, capacity, **status** (0/1/2) | 桌台 |
| categories | name | 签子类别 |
| skewer_types | category_id, name, price, status | 菜单，调价直接 UPDATE |
| orders | order_no, table_id, waiter_id, **zone_surcharge**, **status** (0/1) | 订单，附带加快照 |
| order_items | order_id, skewer_type_id, count, **unit_price**, **subtotal** | 明细，唯一约束防重复，单价快照 |
| operation_logs | user_id, operation_type, target, detail | 管理操作审计 |

**设计要点**：`orders.zone_surcharge` 和 `order_items.unit_price` 开单时快照固化，后续调价不追溯。结账：`total = Σ(subtotal) + surcharge`。SQLite 开发，生产切 PostgreSQL（`DB_URL` 环境变量）。

### 4. 订单状态机

```
空闲(0) ──开台──▶ 占用(1) ──结账──▶ 清洁中(2) ──复位──▶ 空闲(0)
                                   │
                        强制结账（管理员）
```

- 开台：创建订单时自动将桌台设为占用
- 结账：汇总签子数量 + 区域附加费，桌台进入清洁状态
- 复位：仅允许 `清洁中 → 空闲`，防止误操作覆盖占用中的桌面
- order_no 格式：`YYYYMMDDHHmmss-{table_id}`，天然有序且去重

### 5. 前端技术

| | admin | waiter |
|---|---|---|
| UI 库 | Element Plus | Tailwind CSS |
| 图表 | ECharts | — |
| 设计 | 火锅暖色暗黑主题 | 火焰暖色暗黑主题 |
| 渲染 | Desktop 优先 | Mobile-first 响应式 |

- `admin` 使用 **Pinia** 管理全局状态，**Axios 拦截器**处理认证与错误
- `waiter` 纯 Canvas 验证码 → 已改为后端统一验证码接口，**Pinia auth store** 驱动路由守卫
- 两个前端均通过 **Vite proxy** 转发 `/api` 到后端 8000 端口

### 6. 管理后台核心功能

- **Dashboard**：今日订单/签子/营收/占用卡统计 + 饼图（桌台分布）+ 柱状图（热销 TOP5）
- **实时监控**：按区域分组的桌台网格，订单详情弹窗，强制结账
- **用户管理**：CRUD + 启用/禁用开关，操作记录审计日志
- **调价管理**：签子价格表格编辑，调价不追溯已有订单
- **报表**：按日筛选签子销量柱状图 + 每桌营收卡片排行
- **操作日志**：分页查询，按日期/类型/用户筛选，8 种操作类型中文化展示

### 7. 操作审计

`operation_logs` 表记录所有管理操作：

| 操作 | 含义 |
|------|------|
| `price_adjust` | 调价 |
| `user_create/update/disable/enable` | 员工管理 |
| `skewer_online/offline` | 签子上下架 |
| `order_close` | 强制结账 |

每条日志包含操作人、目标对象、详情 JSON、IP 地址、时间戳。

### 8. 开发与部署

- **一键安装**：`python install.py` 并行安装 backend/admin/waiter 三套依赖
- **一键启动**：`python start.py` 以 `subprocess.Popen` 并行启动三个进程，stdout/stderr 分流到 `logs/{service}/output.log` 和 `error.log`
- **热重载**：backend 使用 `uvicorn --reload`，前端使用 Vite HMR
- **CORS**：开发环境全开放
- **测试**：15 个集成测试覆盖认证、菜单、桌台、完整订单流程、权限、调价、用户管理、状态转换、去重等

---

## 功能清单

### 服务员端
- **桌台概览** — 按区域分组展示所有桌台，颜色区分空闲/占用/清洁中，统计卡片实时汇总
- **开台** — 选择桌台创建新订单，自动切换桌台为占用状态
- **点单** — 按分类浏览签子菜单，支持添加菜品到订单
- **AI 拍照计数** — 手机拍照上传，YOLO 模型自动识别签子数量
- **手动调整** — 支持 +/- 按钮或直接输入修改数量
- **结账** — 自动汇总签子总价 + 区域附加费，结账后桌台进入清洁状态
- **清洁复位** — 服务员确认清洁完毕，桌台恢复空闲

### 管理后台
- **数据看板** — 今日订单数、签子销量、营收金额、占用桌台数；饼图（桌台分布）、柱状图（热销 TOP5）
- **实时监控** — 按区域查看所有桌台状态，支持强制结账
- **用户管理** — 管理员/服务员账号 CRUD，启用/禁用切换
- **调价管理** — 签子价格表格编辑，调价不追溯已有订单
- **销售报表** — 按日期查看各签子销量柱状图、每桌营收排行
- **操作日志** — 所有管理操作记录：调价、员工变更、强制结账等，支持按日期/类型/用户筛选
