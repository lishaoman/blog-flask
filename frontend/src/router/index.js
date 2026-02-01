// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// 引入详情页组件
import PostDetail from '../views/PostDetail.vue'
import CreatePost from '../views/CreatePost.vue' // 引入组件
// ... 引入 EditPost
import EditPost from '../views/EditPost.vue'

const router = createRouter({
  // 使用 HTML5 History 模式 (URL 中没有 # 号，更美观)
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // 路由懒加载：只有访问 About 页面时才加载这个组件代码，优化性能
      component: () => import('../views/AboutView.vue')
    },
    // === 新增路由 ===
    {
      // :id 是动态参数
      path: '/post/:id',
      name: 'post-detail',
      component: PostDetail
    },
      // === 新增路由 ===
    {
      path: '/create',
      name: 'create-post',
      component: CreatePost
    },
    {
      path: '/edit/:id',
      name: 'edit-post',
      component: EditPost
    },
    // === 分类和标签路由 ===
    {
      path: '/categories',
      name: 'category-list',
      component: () => import('../views/CategoryList.vue')
    },
    {
      path: '/category/:id',
      name: 'category-posts',
      component: () => import('../views/CategoryPosts.vue')
    },
    {
      path: '/tags',
      name: 'tag-list',
      component: () => import('../views/TagList.vue')
    },
    {
      path: '/tag/:id',
      name: 'tag-posts',
      component: () => import('../views/TagPosts.vue')
    }
  ]
})

export default router