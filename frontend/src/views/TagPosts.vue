<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/index'

const route = useRoute()
const tag = ref(null)
const posts = ref([])
const loading = ref(true)

// 获取标签下的文章列表
const fetchTagPosts = async () => {
  loading.value = true
  try {
    const tagId = route.params.id
    const response = await api.get(`/api/tags/${tagId}/posts`)
    tag.value = response.data.tag
    posts.value = response.data.posts
  } catch (error) {
    console.error('获取标签文章失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTagPosts()
})
</script>

<template>
  <div class="tag-posts">
    <div class="header">
      <h1># {{ tag?.name || '标签' }}</h1>
      <span class="post-count-badge">{{ posts.length }} 篇文章</span>
    </div>

    <div v-if="loading">加载中...</div>

    <div v-else class="post-list">
      <div v-if="posts.length === 0" class="no-data">
        该标签下暂无文章
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
          <span class="category-badge" v-if="post.category && post.category !== '未分类'">
            📂 {{ post.category }}
          </span>
        </div>

        <div class="tags-container" v-if="post.tags && post.tags.length">
          <span v-for="t in post.tags" :key="t" class="tag-badge">
            #{{ t }}
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
  border-bottom: 2px solid #0277bd;
}

.post-count-badge {
  background-color: #e1f5fe;
  color: #0277bd;
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

.category-badge {
  background-color: #eee;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85em;
  color: #555;
  margin-left: 10px;
}

.no-data {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
