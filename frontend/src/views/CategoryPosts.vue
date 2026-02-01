<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/index'

const route = useRoute()
const category = ref(null)
const posts = ref([])
const loading = ref(true)

// 获取分类下的文章列表
const fetchCategoryPosts = async () => {
  loading.value = true
  try {
    const categoryId = route.params.id
    const response = await api.get(`/api/categories/${categoryId}/posts`)
    category.value = response.data.category
    posts.value = response.data.posts
  } catch (error) {
    console.error('获取分类文章失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategoryPosts()
})
</script>

<template>
  <div class="category-posts">
    <div class="header">
      <h1>📂 {{ category?.name || '分类' }}</h1>
      <span class="post-count-badge">{{ posts.length }} 篇文章</span>
    </div>

    <div v-if="loading">加载中...</div>

    <div v-else class="post-list">
      <div v-if="posts.length === 0" class="no-data">
        该分类下暂无文章
      </div>

      <div v-else v-for="post in posts" :key="post.id" class="post-card">
        <h2>
          <router-link :to="{ name: 'post-detail', params: { id: post.id }}">
            {{ post.title }}
          </router-link>
        </h2>

        <p class="excerpt">{{ post.content?.substring(0, 100) }}...</p>

        <div class="meta">
          <small>📅 {{ new Date(post.created_at).toLocaleDateString() }}</small>
        </div>

        <div class="tags-container" v-if="post.tags && post.tags.length">
          <span v-for="tag in post.tags" :key="tag" class="tag-badge">
            #{{ tag }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #42b883;
}

.post-count-badge {
  background-color: #f0f0f0;
  color: #666;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
}

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
.excerpt { color: #666; margin: 10px 0; }

.tags-container { margin-top: 10px; }

.tag-badge {
  display: inline-block;
  background-color: #e1f5fe;
  color: #0277bd;
  font-size: 0.8em;
  padding: 2px 8px;
  border-radius: 12px;
  margin-right: 5px;
}

.no-data {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
