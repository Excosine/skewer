# 自助火锅竹签计价系统 - 管理员前端实施计划

**关联设计文档**: 2026-06-30-admin-frontend-design.md  
**编写日期**: 2026-06-30  
**实施状态**: 待开始

---

## 一、项目初始化

### 1.1 创建前端项目

**操作步骤**:
```powershell
# 1. 进入项目根目录
cd d:\files\大三下课件\大三下\qianzi\skewer-main\skewer-main

# 2. 使用 Vite 创建 Vue3 项目
npm create vite@latest frontend -- --template vue

# 3. 进入前端目录
cd frontend

# 4. 安装核心依赖
npm install element-plus axios echarts vue-router pinia

# 5. 安装开发依赖
npm install -D sass
```

**依赖清单**:
| 包名 | 版本 | 用途 |
|------|------|------|
| vue | 3.x | 核心框架 |
| element-plus | 2.x | UI组件库 |
| axios | 1.x | HTTP请求 |
| echarts | 5.x | 数据可视化 |
| vue-router | 4.x | 路由管理 |
| pinia | 2.x | 状态管理（可选） |
| sass | 1.x | CSS预处理 |

### 1.2 配置 Vite 开发代理

**文件**: frontend/vite.config.js

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

---

## 二、目录结构设置

### 2.1 标准目录结构

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/               # 静态资源
│   │   ├── images/           # 图片
│   │   └── styles/           # 全局样式
│   │       ├── variables.scss  # 颜色/字体变量
│   │       ├── reset.scss      # 样式重置
│   │       └── common.scss     # 公共样式
│   │
│   ├── components/           # 可复用组件
│   │   ├── common/           # 通用组件
│   │   │   ├── Sidebar.vue   # 侧边栏
│   │   │   ├── Header.vue    # 顶部栏
│   │   │   ├── TableCard.vue # 桌况卡片
│   │   │   └── StatCard.vue  # 统计卡片
│   │   │
│   │   ├── layout/           # 布局组件
│   │   │   └── AdminLayout.vue  # 管理后台布局
│   │   │
│   │   └── charts/           # 图表组件
│   │       ├── BarChart.vue  # 柱状图
│   │       └── LineChart.vue # 折线图
│   │
│   ├── views/                # 页面视图
│   │   ├── Login.vue         # 登录页
│   │   ├── Dashboard.vue     # 仪表盘
│   │   ├── Monitor.vue       # 运营监控
│   │   ├── Users.vue         # 员工管理
│   │   ├── Prices.vue        # 价格管理
│   │   ├── Reports.vue       # 数据报表
│   │   └── Settings.vue      # 系统设置
│   │
│   ├── router/               # 路由配置
│   │   └ index.js            # 路由定义
│   │
│   ├── api/                  # API请求
│   │   ├── request.js        # Axios封装
│   │   ├── auth.js           # 认证API
│   │   ├── admin.js          # 管理API
│   │   └ table.js            # 桌况API
│   │   └ menu.js             # 菜单API
│   │   └ report.js           # 报表API
│   │
│   ├── store/                # 状态管理（Pinia）
│   │   ├── user.js           # 用户状态
│   │   └ theme.js            # 主题状态
│   │
│   ├── utils/                # 工具函数
│   │   ├── auth.js           # Token管理
│   │   ├── theme.js          # 主题切换
│   │   ├── date.js           # 日期格式化
│   │
│   ├── App.vue               # 根组件
│   ├── main.js               # 入口文件
│   │
├── index.html                # HTML入口
├── vite.config.js            # Vite配置
├── package.json              # 依赖配置
└── README.md                 # 项目说明
```

---

## 三、分阶段实施计划

### 第一阶段：项目基础搭建（预计 2 小时）

**任务清单**:
1. ✅ 创建 Vue3 项目
2. ✅ 安装所有依赖
3. ✅ 配置 Vite 代理
4. ✅ 创建目录结构
5. ✅ 编写全局样式变量
6. ✅ 配置 ElementPlus 暗色模式

**关键文件**:

| 文件路径 | 功能 |
|----------|------|
| src/assets/styles/variables.scss | 定义暖色系配色变量 |
| src/assets/styles/reset.scss | 样式重置，禁止响应式 |
| src/assets/styles/common.scss | 公共样式类 |
| src/main.js | 注册 ElementPlus，配置主题 |

**样式变量文件**: src/assets/styles/variables.scss
```scss
// 主题色系（火锅温暖感）
$primary-orange: #F97316;    // 主题橙
$primary-orange-dark: #EA580C; // hover强调
$primary-orange-light: #FED7AA; // 淡橙背景
$primary-orange-hover: #FFF7ED; // hover背景

// 成功色（火锅红）
$success-red: #DC2626;       // 营业额数字
$success-red-light: #FEE2E2; // 浅红背景

// 中性色
$text-primary: #1F2937;      // 主文字
$text-secondary: #6B7280;    // 次文字
$text-tertiary: #9CA3AF;     // 辅助文字
$border-color: #E5E7EB;      // 边框
$bg-light: #F9FAFB;          // 淡灰背景
$card-bg: #FFFFFF;           // 卡片背景

// 状态色
$warning-orange: #F59E0B;    // 清洁中
$info-blue: #3B82F6;         // 图表蓝

// 状态色（桌况）
$table-idle: #D1D5DB;        // 空闲灰
$table-occupied: #DC2626;    // 占用红
$table-cleaning: #F59E0B;    // 清洁橙

// 暗色模式变量
$dark-bg: #111827;
$dark-card-bg: #1F2937;
$dark-border: #374151;
$dark-text-primary: #F9FAFB;
$dark-text-secondary: #D1D5DB;

// 字体
$font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
$font-mono: "SF Mono", "Consolas", monospace;

// 间距（8px base）
$spacing-xs: 8px;
$spacing-s: 12px;
$spacing-m: 16px;
$spacing-l: 24px;
$spacing-xl: 32px;

// 固定尺寸
$sidebar-width: 200px;
$header-height: 64px;
$stat-card-width: 240px;
$stat-card-height: 120px;
$table-card-size: 64px;
```

---

### 第二阶段：核心组件开发（预计 4 小时）

**任务清单**:
1. ✅ 开发 AdminLayout 布局组件
2. ✅ 开发 Header 顶部栏组件
3. ✅ 开发 Sidebar 侧边栏组件
4. ✅ 开发 StatCard 统计卡片组件
5. ✅ 开发 TableCard 桌况卡片组件
6. ✅ 开发 BarChart 柱状图组件
7. ✅ 开发弹窗组件（基于 ElementPlus Dialog）

**组件开发顺序**:
```
1. AdminLayout.vue  → 布局容器，侧边栏+顶部栏+内容区
2. Header.vue       → Logo + 主题切换 + 用户信息
3. Sidebar.vue      → 导航菜单 + 选中态
4. StatCard.vue     → 数据统计卡片（4种状态）
5. TableCard.vue    → 桌况卡片（3种状态）
6. BarChart.vue     → ECharts柱状图封装
```

**组件规格示例**: src/components/common/Sidebar.vue

```
功能要求：
  - 固定宽度 200px
  - 6个导航项：仪表盘、运营监控、员工管理、价格管理、数据报表、系统设置
  - 选中态：浅橙背景 + 左侧橙色竖线
  - hover态：淡橙背景 + 文字橙色
  - 使用 ElementPlus Menu 组件

技术实现：
  - 使用 ElementPlus el-menu 组件
  - 自定义样式覆盖默认配色
  - Vue Router 集成，router-link 导航
  - 监听路由变化，更新选中项
```

---

### 第三阶段：页面开发（预计 6 小时）

**开发顺序**:

| 页面 | 文件路径 | 核心功能 | 预计耗时 |
|------|----------|----------|----------|
| 登录页 | src/views/Login.vue | 登录表单 + Token存储 | 1小时 |
| 仪表盘 | src/views/Dashboard.vue | 4个统计卡片 + 桌况网格 + 热销排行 | 2小时 |
| 运营监控 | src/views/Monitor.vue | 桌况网格 + 区域筛选 + 订单详情弹窗 | 1小时 |
| 员工管理 | src/views/Users.vue | 员工表格 + 新增/编辑弹窗 | 1小时 |
| 价格管理 | src/views/Prices.vue | 签子表格 + 调价弹窗 | 0.5小时 |
| 数据报表 | src/views/Reports.vue | Tab切换 + 图表 + 表格 + 日期筛选 | 1.5小时 |

**关键页面详情**: src/views/Dashboard.vue

```
组件组合：
  - 顶部：页面标题"仪表盘"
  - 第一行：4个 StatCard 组件（横向排列）
    - 今日订单数（橙色数字）
    - 今日签子数（橙色数字）
    - 今日营业额（红色数字）
    - 当前桌况（橙色数字）
  - 第二行：实时桌况分布图
    - 使用 TableCard 网格布局
    - 按区域分组：大厅、包间、露台
  - 第三行：今日热销排行
    - TOP 3 列表展示
  - 第四行：快捷操作按钮
    - 4个次要按钮横向排列

数据获取：
  - 调用 API: /api/tables（桌况）
  - 调用 API: /api/admin/reports/skewers（销量）
  - 调用 API: /api/admin/reports/tables（营业额）
  - 手动刷新按钮，不自动轮询
```

---

### 第四阶段：API对接（预计 3 小时）

**API封装文件**:

| 文件 | 功能 | 对应后端路由 |
|------|------|--------------|
| src/api/request.js | Axios封装 + Token携带 + 错误处理 | 全局拦截器 |
| src/api/auth.js | 登录、获取用户信息 | /api/auth/login, /api/auth/me |
| src/api/admin.js | 用户管理、调价、报表 | /api/admin/* |
| src/api/table.js | 桌况查询 | /api/tables |
| src/api/menu.js | 签子列表 | /api/menu/skewers |
| src/api/report.js | 销量/营业额报表 | /api/admin/reports/* |

**request.js 核心实现**:
```javascript
import axios from 'axios'
import router from '@/router'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截：携带Token
request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：错误处理
request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default request
```

---

### 第五阶段：路由和状态管理（预计 1 小时）

**路由配置**: src/router/index.js

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    component: AdminLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'monitor',
        name: 'Monitor',
        component: () => import('@/views/Monitor.vue'),
        meta: { title: '运营监控' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/Users.vue'),
        meta: { title: '员工管理' }
      },
      {
        path: 'prices',
        name: 'Prices',
        component: () => import('@/views/Prices.vue'),
        meta: { title: '价格管理' }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/Reports.vue'),
        meta: { title: '数据报表' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue'),
        meta: { title: '系统设置' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：Token验证
router.beforeEach((to, from, next) => {
  if (to.path !== '/login' && !localStorage.getItem('token')) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

**状态管理**: src/store/user.js

```javascript
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: '',
    role: '',
    realName: ''
  }),
  
  actions: {
    setUser(userData) {
      this.token = userData.token
      this.username = userData.username
      this.role = userData.role
      this.realName = userData.real_name
      localStorage.setItem('token', userData.token)
    },
    
    logout() {
      this.token = ''
      this.username = ''
      this.role = ''
      this.realName = ''
      localStorage.removeItem('token')
    }
  }
})
```

---

### 第六阶段：测试和调试（预计 2 小时）

**测试清单**:

| 测试项 | 测试内容 | 预期结果 |
|--------|----------|----------|
| 登录流程 | 输入用户名密码 | Token存储，跳转仪表盘 |
| Token失效 | 401响应 | 清除Token，跳转登录页 |
| 路由守卫 | 无Token访问管理页 | 跳转登录页 |
| 桌况显示 | 访问运营监控 | 桌卡网格正确显示 |
| 调价操作 | 修改签子价格 | API调用成功，表格更新 |
| 主题切换 | 切换暗色/浅色 | 所有组件配色切换 |
| 视窗检测 | 缩小浏览器至<1280px | 显示提示遮罩 |

**测试脚本**:
```powershell
# 1. 启动后端
cd backend
python server.py

# 2. 启动前端
cd frontend
npm run dev

# 3. 访问 http://localhost:3000/login
# 4. 使用 admin 账号登录（需先在后端创建）
```

---

### 第七阶段：部署准备（预计 1 小时）

**部署方案**:

#### 开发环境
```
前端：npm run dev (localhost:3000)
后端：python server.py (localhost:8000)
代理：Vite proxy 转发 /api 到后端
```

#### 生产环境
```
前端构建：
  npm run build
  生成 dist/ 目录

部署方式：
  1. nginx 反向代理
     - /api → 后端 8000
     - / → 前端静态文件
  2. 或使用单个 FastAPI 服务前端静态文件
```

**nginx 配置示例**:
```nginx
server {
    listen 80;
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

---

## 四、实施时间规划

| 阶段 | 预计耗时 | 依赖项 |
|------|----------|--------|
| 第一阶段：项目基础搭建 | 2小时 | 无 |
| 第二阶段：核心组件开发 | 4小时 | 第一阶段完成 |
| 第三阶段：页面开发 | 6小时 | 第二阶段完成 |
| 第四阶段：API对接 | 3小时 | 第三阶段完成 |
| 第五阶段：路由和状态管理 | 1小时 | 第四阶段完成 |
| 第六阶段：测试和调试 | 2小时 | 第五阶段完成 |
| 第七阶段：部署准备 | 1小时 | 第六阶段完成 |

**总计**: 19小时（约3个工作日）

---

## 五、风险和应对

### 5.1 技术风险

| 风险项 | 可能影响 | 应对方案 |
|--------|----------|----------|
| ElementPlus 暗色模式配置复杂 | 主题切换不生效 | 参考官方文档，使用 CSS变量覆盖 |
| ECharts 配色冲突 | 图表颜色不符合设计 | 使用自定义配色，不依赖默认主题 |
| 固定尺寸在不同显示器表现 | 1920px 显示器过于紧凑 | 调整间距，使用比例缩放（不改变固定尺寸原则） |
| Token 失效处理不及时 | 用户操作中断 | 在关键操作前验证Token有效性 |

### 5.2 业务风险

| 风险项 | 可能影响 | 应对方案 |
|--------|----------|----------|
| 后端API尚未实现完整管理功能 | 前端功能无法完整测试 | 先模拟数据，待后端完善后对接 |
| 管理员账号未创建 | 无法测试登录流程 | 在测试阶段手动创建admin账号 |
| 暗色模式下火锅红辨识度降低 | 营业额数字不够醒目 | 暗色模式调整红色亮度 |

### 5.3 权限和安全风险

| 风险项 | 可能影响 | 应对方案 |
|--------|----------|----------|
| 操作无日志记录 | 无法追溯管理员操作历史 | 后端API层增加操作日志表，前端显示日志查询界面 |
| Token 被窃取 | 非管理员登录系统 | 使用 HTTPS，设置 Token 过期时间24小时 |
| 权限控制不足 | 服务员访问管理员功能 | 前端路由守卫检查 role，后端API二次验证 |
| XSS攻击风险 | 注入恶意代码 | 使用 Vue3 自动转义，避免直接操作 DOM |

**操作日志记录实现方案**:

需要增加以下功能：
1. **后端数据库新增操作日志表**
   ```sql
   CREATE TABLE operation_logs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER NOT NULL,
       operation_type VARCHAR(32) NOT NULL,  -- 'price_adjust', 'user_create', 'order_close'
       target_id INTEGER,                     -- 操作对象ID
       detail TEXT,                           -- 操作详情JSON
       created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
   );
   ```

2. **后端API增加日志记录中间件**
   - 关键操作（调价、新增员工、结账）自动记录日志
   - 返回操作日志查询接口 `/api/admin/logs`

3. **前端新增日志查询页面**
   - 路由：`/admin/logs`
   - 显示操作时间、操作人、操作类型、操作详情
   - 支持按日期筛选

### 5.4 数据传输风险

| 风险项 | 可能影响 | 应对方案 |
|--------|----------|----------|
| 一月报表数据量大 | 查询慢，前端渲染卡顿 | 分页查询，每页50条；前端分页显示 |
| API请求失败无重试 | 网络波动导致操作失败 | 关键操作（结账、调价）失败时提示重试 |

**报表大数据量应对方案**:

1. **后端API增加分页参数**
   ```
   GET /api/admin/reports/skewers?date=2026-06-01&page=1&page_size=50
   ```

2. **前端使用分页组件**
   - ElementPlus Pagination 组件
   - 每页显示50条数据
   - 避免一次性渲染所有数据

3. **日期范围限制（可选）**
   - 如需查询多月数据，提醒用户分月查询
   - 或导出Excel功能（后端生成，前端下载）

### 5.5 用户体验风险

| 风险项 | 可能影响 | 应对方案 |
|--------|----------|----------|
| 加载状态不明确 | 用户不知道数据正在加载 | 所有异步操作显示骨架屏或加载提示 |
| 操作反馈不明显 | 用户不确定操作是否成功 | 使用 Toast 提示，重要操作显示确认弹窗 |
| 错误提示不友好 | 用户不知道如何处理错误 | 显示具体错误原因和解决建议 |

### 5.6 范围排除说明

以下风险项根据实际场景已排除：

- ❌ **浏览器兼容性风险**：仅支持现代浏览器（Chrome/Edge/Firefox），无需兼容IE
- ❌ **性能风险（桌卡渲染）**：预计20桌台，无需虚拟滚动优化
- ❌ **数据一致性风险（多管理员并发）**：无多管理员同时操作场景，无需乐观锁

---

## 六、操作日志系统设计

### 6.1 数据库表设计

**操作日志表 (operation_logs)**

符合现有 schema.sql 的 BCNF 规范：

```sql
-- ============================================================
-- 9. 操作日志表（新增）
-- ============================================================
CREATE TABLE operation_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),   -- 操作人
    operation_type  VARCHAR(32) NOT NULL,                    -- 操作类型
    target_type     VARCHAR(32),                              -- 操作对象类型
    target_id       INTEGER,                                  -- 操作对象ID（可选）
    detail          TEXT,                                     -- 操作详情JSON
    ip_address      VARCHAR(64),                              -- 操作IP地址（可选）
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_operation_logs_user ON operation_logs(user_id, created_at);
CREATE INDEX idx_operation_logs_type ON operation_logs(operation_type, created_at);
CREATE INDEX idx_operation_logs_time ON operation_logs(created_at DESC);
```

**字段说明**：

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | INTEGER | 主键 | 自增 |
| user_id | INTEGER | 操作人ID | 关联 users.id |
| operation_type | VARCHAR(32) | 操作类型 | 'price_adjust' |
| target_type | VARCHAR(32) | 操作对象类型 | 'skewer', 'user', 'order' |
| target_id | INTEGER | 操作对象ID | 签子ID、员工ID、订单ID |
| detail | TEXT | 操作详情JSON | {"old_price":3.00,"new_price":3.50} |
| ip_address | VARCHAR(64) | 操作IP | '192.168.1.100'（可选） |
| created_at | TIMESTAMP | 操作时间 | 自动记录 |

### 6.2 API接口设计

**查询操作日志接口**: `GET /api/admin/logs`

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 否 | 日期筛选，格式 YYYY-MM-DD，默认今天 |
| operation_type | string | 否 | 操作类型筛选，不传则查全部 |
| user_id | int | 否 | 操作人筛选，不传则查全部 |
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页条数，默认 50，最大 100 |

**响应格式**：`200 OK`

```json
{
  "total": 150,
  "page": 1,
  "page_size": 50,
  "logs": [
    {
      "id": 101,
      "user_id": 1,
      "username": "admin",
      "real_name": "张经理",
      "operation_type": "price_adjust",
      "operation_name": "调价",
      "target_type": "skewer",
      "target_id": 1,
      "target_name": "牛肉串",
      "detail": {
        "old_price": 3.00,
        "new_price": 3.50
      },
      "ip_address": "192.168.1.100",
      "created_at": "2026-06-30T15:30:00"
    }
  ]
}
```

### 6.3 操作类型映射表

| operation_type | operation_name | 描述 |
|----------------|----------------|------|
| price_adjust | 调价 | 修改签子价格 |
| skewer上架 | 上架签子 | 停售签子重新上架 |
| skewer下架 | 下架签子 | 在售签子改为停售 |
| user_create | 新增员工 | 创建新员工账号 |
| user_update | 编辑员工 | 修改员工信息或密码 |
| user_disable | 禁用员工 | 员工账号改为禁用状态 |
| user_enable | 启用员工 | 员工账号改为启用状态 |
| order_close | 强制结账 | 管理员强制结账订单 |

### 6.4 日志记录触发时机

| 操作 | API接口 | operation_type | 触发时机 |
|------|---------|----------------|----------|
| 调价 | PUT /api/admin/skewers/{id}/price | price_adjust | 价格修改成功后 |
| 上架签子 | PUT /api/admin/skewers/{id}/上架 | skewer上架 | 状态改为在售后 |
| 下架签子 | PUT /api/admin/skewers/{id}/下架 | skewer下架 | 状态改为停售后 |
| 新增员工 | POST /api/admin/users | user_create | 用户创建成功后 |
| 编辑员工 | PUT /api/admin/users/{id} | user_update | 用户信息修改成功后 |
| 禁用员工 | PUT /api/admin/users/{id} | user_disable | status改为0后 |
| 启用员工 | PUT /api/admin/users/{id} | user_enable | status改为1后 |
| 强制结账 | POST /api/orders/{id}/close | order_close | 管理员强制结账成功后 |

### 6.5 前端对接

**新增API文件**：src/api/log.js

```javascript
import request from './request'

// 查询操作日志
export function getLogs(params) {
  return request({
    url: '/admin/logs',
    method: 'get',
    params: {
      date: params.date,
      operation_type: params.type,
      user_id: params.userId,
      page: params.page,
      page_size: params.pageSize
    }
  })
}
```

**新增页面文件**：src/views/Logs.vue

显示字段：
- 操作时间：created_at
- 操作人：real_name
- 操作类型：operation_name
- 操作对象：target_name
- 详情：detail（可展开JSON）

---

## 七、关键文件清单

**必创建文件（共 37 个）**:

**样式文件（3个）**:
- src/assets/styles/variables.scss
- src/assets/styles/reset.scss
- src/assets/styles/common.scss

**组件文件（8个）**:
- src/components/layout/AdminLayout.vue
- src/components/common/Header.vue
- src/components/common/Sidebar.vue
- src/components/common/StatCard.vue
- src/components/common/TableCard.vue
- src/components/charts/BarChart.vue
- src/components/charts/LineChart.vue
- src/components/common/EmptyState.vue（空状态）

**页面文件（8个）**:
- src/views/Login.vue
- src/views/Dashboard.vue
- src/views/Monitor.vue
- src/views/Users.vue
- src/views/Prices.vue
- src/views/Reports.vue
- src/views/Logs.vue（操作日志）
- src/views/Settings.vue

**API文件（7个）**:
- src/api/request.js
- src/api/auth.js
- src/api/admin.js
- src/api/table.js
- src/api/menu.js
- src/api/report.js
- src/api/log.js（操作日志）

**配置文件（3个）**:
- src/router/index.js
- src/store/user.js
- src/store/theme.js

**工具文件（3个）**:
- src/utils/auth.js
- src/utils/theme.js
- src/utils/date.js

**入口文件（3个）**:
- src/main.js
- src/App.vue
- vite.config.js

---

## 八、下一步行动

### 8.1 立即开始

**第一步操作**:
```powershell
# 创建项目并安装依赖
cd d:\files\大三下课件\大三下\qianzi\skewer-main\skewer-main
npm create vite@latest frontend -- --template vue
cd frontend
npm install element-plus axios echarts vue-router pinia sass
```

### 8.2 实施建议

1. **按阶段顺序实施**，不跳跃阶段
2. **每个阶段完成后进行简单测试**，确保功能正常
3. **遇到问题及时记录**，避免重复调试
4. **核心组件优先开发**，复用性高的组件先完成
5. **API对接前准备好模拟数据**，确保前端逻辑完整

---

## 九、文档状态

- 实施计划编写日期：2026-06-30
- 实施状态：待开始
- 预计总耗时：19小时
- 文档版本：v1.0
- 文档路径：docs/superpowers/specs/2026-06-30-admin-frontend-implementation-plan.md

---

**文档结束**