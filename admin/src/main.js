import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css' // 暗色模式支持
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 全局样式
import './assets/styles/variables.scss'
import './assets/styles/reset.scss'
import './assets/styles/common.scss'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// 注册 ElementPlus
app.use(ElementPlus)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 注册路由
app.use(router)

app.mount('#app')
