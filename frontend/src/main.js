import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 引入路由配置


// 引入基础样式 (可选，如果你刚才清空了 style.css，这里可以先注释掉)
// import './style.css'

const app = createApp(App)

app.use(router) // 告诉 Vue 使用这个路由

app.mount('#app')