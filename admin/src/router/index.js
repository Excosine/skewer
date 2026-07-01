import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/',
    component: () => import('@/components/layout/AdminLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘', requiresAuth: true }
      },
      {
        path: 'monitor',
        name: 'Monitor',
        component: () => import('@/views/Monitor.vue'),
        meta: { title: '运营监控', requiresAuth: true }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/Users.vue'),
        meta: { title: '员工管理', requiresAuth: true }
      },
      {
        path: 'prices',
        name: 'Prices',
        component: () => import('@/views/Prices.vue'),
        meta: { title: '价格管理', requiresAuth: true }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/Reports.vue'),
        meta: { title: '数据报表', requiresAuth: true }
      },
      {
        path: 'logs',
        name: 'Logs',
        component: () => import('@/views/Logs.vue'),
        meta: { title: '操作日志', requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：Token验证
router.beforeEach((to) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 竹签计价系统` : '竹签计价系统'
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    return '/login'
  }
  
  // 已登录时访问登录页，跳转到首页
  if (to.path === '/login' && localStorage.getItem('token')) {
    return '/dashboard'
  }
  
  // 正常放行
  return true
})

export default router