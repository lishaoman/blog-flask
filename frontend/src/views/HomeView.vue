<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index'

const posts = ref([])
const loading = ref(true)

// 获取文章列表
const fetchPosts = async () => {
  try {
    const response = await api.get('/api/posts')
    posts.value = response.data
  } catch (error) {
    console.error('获取列表失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <div class="home">
    <div class="header">
      <h1>📃 最新文章</h1>
    </div>

    <div v-if="loading">加载中...</div>

    <div v-else class="post-list">
      <div v-if="posts.length === 0">暂无文章，快去写一篇吧！</div>

      <div v-for="post in posts" :key="post.id" class="post-card">
        <h2>
          <router-link :to="{ name: 'post-detail', params: { id: post.id }}">
            {{ post.title }}
          </router-link>
        </h2>
        <p class="excerpt">{{ post.content.substring(0, 100) }}...</p>
        <div class="meta">
          <small>{{ new Date(post.created_at).toLocaleDateString() }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.post-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  transition: transform 0.2s;
  background: white;
}
.post-card:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.post-card h2 { margin-top: 0; font-size: 1.5rem; }
.post-card h2 a { text-decoration: none; color: #2c3e50; }
.post-card h2 a:hover { color: #42b883; }
.excerpt { color: #666; }
</style>