<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router' // 用于获取 URL 参数
import api from '../api/index'

// 引入 Markdown 解析器和清洗器
import { marked } from 'marked'
import DOMPurify from 'dompurify'

// 引入 GitHub 风格的 Markdown 样式
import 'github-markdown-css/github-markdown-light.css'

const route = useRoute()
const post = ref(null)
const loading = ref(true)
const error = ref('')

// 计算属性：将 markdown 内容转换为安全的 HTML
const renderedContent = computed(() => {
  if (!post.value || !post.value.content) return ''
  // 1. 解析 Markdown
  const rawHtml = marked.parse(post.value.content)
  // 2. 清洗 HTML (防止 XSS 攻击)
  return DOMPurify.sanitize(rawHtml)
})

onMounted(async () => {
  const postId = route.params.id // 获取路由中的 id 参数
  try {
    const response = await api.get(`/api/posts/${postId}`)
    post.value = response.data
  } catch (err) {
    error.value = '文章加载失败，可能文章不存在。'
    console.error(err)
  } finally {
    loading.value = false
  }
})

// 添加删除函数
const deletePost = async () => {
  if (!confirm('确定要删除这篇文章吗？此操作不可恢复！😱')) return

  try {
    await api.delete(`/api/posts/${post.value.id}`)
    alert('删除成功 🗑️')
    route.push('/') // 删完回首页
  } catch (error) {
    console.error(error)
    alert('删除失败')
  }
}
</script>

<template>
  <div class="post-detail">
    <div v-if="loading" class="loading">⏳ 加载中...</div>

    <div v-else-if="error" class="error">❌ {{ error }}</div>

    <div v-else-if="post" class="content">
      <h1 class="title">{{ post.title }}</h1>
      <div class="meta">
        <span>发布于: {{ new Date(post.created_at).toLocaleString() }}</span>
      </div>
      <div class="body markdown-body" v-html="renderedContent">
      </div>

      <div class="actions">
        <router-link to="/" class="back-btn">⬅️ 返回列表</router-link>

        <div class="admin-actions">
          <router-link
            :to="{ name: 'edit-post', params: { id: post.id }}"
            class="edit-btn"
          >
            ✏️ 编辑
          </router-link>

          <button @click="deletePost" class="delete-btn">🗑️ 删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.post-detail { max-width: 800px; margin: 0 auto; }
.meta { color: #888; font-size: 0.9em; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
.body p { line-height: 1.6; white-space: pre-wrap; }
.back-btn { display: inline-block; margin-top: 20px; text-decoration: none; color: #42b883; }
/* 覆盖一些 markdown 样式以适应我们的布局 */
.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 15px;
}
.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}
.admin-actions { display: flex; gap: 10px; }
.edit-btn {
  text-decoration: none;
  background: #3498db;
  color: white;
  padding: 8px 15px;
  border-radius: 4px;
  font-size: 0.9em;
}
.delete-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}
.delete-btn:hover { background: #c0392b; }
</style>