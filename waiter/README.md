# 签子计数 — 服务员端 (Waiter)

基于 Vue 3 + Vite + Tailwind CSS 构建的手机端/桌面端响应式服务员工作台。

## 技术栈

| 类别       | 技术                                |
| ---------- | ----------------------------------- |
| 框架       | Vue 3 (Composition API + `<script setup>`) |
| 构建工具   | Vite 6                              |
| 路由       | vue-router 4                        |
| 状态管理   | Pinia 3                             |
| 样式       | Tailwind CSS 3 (scoped CSS 局部覆盖) |

## 项目结构

```
waiter/
├── index.html                 # 入口 HTML
├── vite.config.js             # Vite 配置（含 API 代理）
├── tailwind.config.js         # Tailwind 主题扩展
├── postcss.config.js          # PostCSS 插件
├── package.json
└── src/
    ├── main.js                # 应用入口，挂载 Pinia + Router
    ├── App.vue                # 根组件，提供全局 Toast
    ├── style.css              # Tailwind 指令入口
    ├── api/
    │   └── index.js           # 统一 API 请求层
    ├── router/
    │   └── index.js           # 路由定义 + 导航守卫
    ├── stores/
    │   └── auth.js            # Pinia 认证状态
    ├── composables/
    │   └── useToast.js        # Toast 注入钩子
    ├── components/
    │   ├── AppHeader.vue      # 顶栏（标题/返回/退出）
    │   ├── MenuPicker.vue     # 菜品选择弹窗（按分类筛选）
    │   └── Toast.vue          # 轻提示 + 确认对话框
    └── pages/
        ├── LoginPage.vue      # 登录 — 黑红炭火火焰主题
        ├── RegisterPage.vue   # 注册（含图形验证码）
        ├── TablesPage.vue     # 桌台列表 — 深色火焰主题
        ├── TableDetailPage.vue# 桌台详情（开单/打扫/历史）
        └── OrderDetailPage.vue# 订单详情（加菜/扫码/结账）
```

## 路由

| 路径            | 页面              | 说明     |
| --------------- | ----------------- | -------- |
| `/login`        | LoginPage         | 公开     |
| `/register`     | RegisterPage      | 公开     |
| `/`             | TablesPage        | 需登录   |
| `/tables/:id`   | TableDetailPage   | 需登录   |
| `/orders/:id`   | OrderDetailPage   | 需登录   |

未登录访问需认证的路由自动跳转 `/login`。

## Tailwind 主题色

定义于 `tailwind.config.js`：

| Token        | 值          | 用途                 |
| ------------ | ----------- | -------------------- |
| `surface`    | `#121010`   | 主背景色             |
| `cream`      | `#F5EFE4`   | 标题/正文亮色        |
| `muted`      | `#C9A77A`   | 辅助文字/次要信息    |
| `brand-*`    | 橙红系      | 主品牌色（火焰色）   |
| `flame-*`    | 同 brand    | 品牌色别名           |

## API 接口

所有请求通过 `src/api/index.js` 统一封装，自动携带 `Bearer Token`。

### 认证

| 方法     | 端点                  | 说明         |
| -------- | --------------------- | ------------ |
| `POST`   | `/api/auth/login`     | 登录         |
| `POST`   | `/api/auth/register`  | 注册         |
| `GET`    | `/api/auth/me`        | 获取当前用户 |

### 桌台

| 方法     | 端点                     | 说明           |
| -------- | ------------------------ | -------------- |
| `GET`    | `/api/tables`            | 获取所有桌台   |
| `GET`    | `/api/tables/:id`        | 获取桌台详情   |
| `PUT`    | `/api/tables/:id`        | 更新桌台状态   |

### 菜品

| 方法  | 端点                    | 说明           |
| ----- | ----------------------- | -------------- |
| `GET` | `/api/menu/categories`  | 获取菜品分类   |
| `GET` | `/api/menu/skewers`     | 获取所有签子   |

### 订单

| 方法     | 端点                              | 说明         |
| -------- | --------------------------------- | ------------ |
| `POST`   | `/api/orders`                     | 创建订单     |
| `GET`    | `/api/orders/:id`                 | 获取订单详情 |
| `POST`   | `/api/orders/:id/close`           | 结账         |
| `POST`   | `/api/orders/:oid/items`          | 添加菜品     |
| `PUT`    | `/api/orders/:oid/items/:iid`     | 更新菜品数量 |
| `DELETE` | `/api/orders/:oid/items/:iid`     | 删除菜品     |
| `POST`   | `/api/orders/:oid/items/:iid/scan`| 拍照扫码识别数量 |

## 页面功能说明

### 登录 (`/login`)

黑红炭火火焰主题，纯 CSS 实现无外部依赖：

- **背景**：`#121010` 炭黑 + 四角径向暗红橙光晕 + 低透明度食材点阵纹理 + SVG 噪点
- **弹窗**：居中 `max-w-[440px]` 磨砂玻璃，`rgba(32,20,18,0.75)` 半透深红棕底，`backdrop-blur(24px)`
- **边框**：`conic-gradient` 动画旋转火焰描边（`4s` 正转 + `6s` 反转），多层径向光晕
- **Logo**：56px 橙红渐变方形火焰 SVG，`box-shadow` 外发光
- **标题**：28px 800w 渐变字 `#F5EFE4→#FFD700→#FF8C42→#FF4A22`
- **表单**：深色半透输入框 `rgba(0,0,0,0.45)` + 细橙红边框，用户名/密码 SVG 图标，密码眼显隐切换
- **验证码**：Canvas 深棕底 + 火焰色字符 `shadowBlur` 发光 + 噪点干扰线
- **按钮**：火焰橙红渐变宽幅按钮 + `box-shadow` 外发光，hover 增强亮度
- **底部**：默认账号 admin/123456、waiter01/123456 展示

### 注册 (`/register`)

- 同登录页布局风格，含用户名、姓名、密码、验证码字段
- 注册成功自动跳转登录页

### 桌台列表 (`/`)

深色火焰主题，`#121010` 背景 + 径向渐变光晕：

- 左侧大屏毛玻璃侧边栏 `rgba(42,26,22,0.55)`，手机端顶部栏
- 概览卡片：玻璃态风格 + brand 色边框
- 状态分布面板：渐变色进度条（空闲绿 / 占用橙红 / 清洁灰）
- 桌台卡片按区域分区展示，CSS 类 `tc-0/1/2` 分别控制状态边框色和阴影
- 文字色值：标题 `#F5EFE4`，次要 `#C9A77A`，品牌 `#ff8c42`/`#ff4a22`

桌台状态：0=空闲（绿边），1=占用（橙红粗边 + 发光），2=清洁中（灰边）

### 桌台详情 (`/tables/:id`)

- 展示桌台代码、区域、容量、加价
- 空闲 →「开单」按钮
- 占用 → 跳转进行中订单
- 清洁 →「完成打扫」
- 底部历史结账记录

### 订单详情 (`/orders/:id`)

- 菜品列表：加减数量、小计、删除
-「加菜」打开 `MenuPicker` 滑出式弹窗（按分类筛选菜品）
- 拍照扫码识别数量（调用 `/scan` 接口，上传图片返回 `detected_count`）
- 订单为空 →「取消订单」
- 底部/侧边订单汇总 +「结账」按钮
- 结账后跳转回桌台详情

## 开发

```bash
cd waiter
npm install
npm run dev
```

开发服务器 `http://localhost:5173`，API 代理到 `http://localhost:8000`。

## 构建

```bash
npm run build
```

产物输出到 `dist/` 目录。
