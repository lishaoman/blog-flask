<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../api/index'

const posts = ref([])
const loading = ref(true)
// === 新增状态变量 ===
const searchQuery = ref('') // 搜索关键词
const isSearching = ref(false) // 是否处于搜索模式

// 获取文章列表
const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/posts/')
    posts.value = response.data
    isSearching.value = false
  } catch (error) {
    console.error('获取列表失败:', error)
  } finally {
    loading.value = false
  }
}

// === 新增搜索处理函数 ===
const handleSearch = async () => {
  const query = searchQuery.value.trim()

  // 如果搜索框为空，则恢复加载全量列表
  if (!query) {
    fetchPosts()
    return
  }

  loading.value = true
  isSearching.value = true
  try {
    // 调用我们之前设计的后端搜索接口
    const response = await api.get(`/api/posts/search?q=${encodeURIComponent(query)}`)
    posts.value = response.data
  } catch (error) {
    console.error('搜索失败:', error)
    posts.value = [] // 报错时清空列表
  } finally {
    loading.value = false
  }
}

// === 新增清空函数 ===
const clearSearch = () => {
  searchQuery.value = ''
  fetchPosts()
}

// === 新增防抖搜索 (可选) ===
// 当用户输入停止 500ms 后自动触发搜索，无需频繁点击回车
let timer = null
watch(searchQuery, (newVal) => {
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => {
    handleSearch()
  }, 500)
})

// === 新增：关键词高亮匹配函数 ===
// 参数 text: 原始文本 (如文章标题或内容摘要)
const highlightMatcher = (text) => {
  // 1. 如果文本为空，或当前没有搜索词，或不在搜索模式下，直接返回原文本
  if (!text || !searchQuery.value || !isSearching.value) {
    // 为了安全起见，这里简单转义一下 HTML 标签，防止 XSS（生产环境建议用 DOMPurify）
    return text ? text.replace(/</g, "&lt;").replace(/>/g, "&gt;") : '';
  }

  const query = searchQuery.value.trim();
  if (!query) return text;

  try {
    // 2. 转义正则表达式中的特殊字符，防止用户输入 ". * + ?" 等符号导致报错
    // 例如用户搜 ".", 我们需要转义成 "\." 才能当作普通小数点匹配
    const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    // 3. 创建正则表达式：全局匹配 (g), 忽略大小写 (i)
    // 使用捕获组 () 将匹配到的内容包裹起来，以便在替换时引用它
    const regex = new RegExp(`(${escapedQuery})`, 'gi');

    // 4. 执行替换
    // $1 代表正则中第一个捕获组匹配到的实际文本（保留原文的大小写）
    // 我们将它包裹在带有特定类的 span 标签中
    return text.replace(regex, '<span class="highlight-keyword">$1</span>');

  } catch (e) {
    // 万一正则构建失败，返回原文本作为回退方案
    console.error('Highlight error:', e);
    return text;
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

    <div class="search-container">
      <input
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        placeholder="搜索文章标题或内容..."
        class="search-input"
      />
      <button @click="handleSearch" class="search-button">搜索</button>
      <button v-if="searchQuery" @click="clearSearch" class="clear-button">清空</button>
    </div>

    <h1>{{ isSearching ? '🔍 搜索结果' : '最新文章' }}</h1>

    <div v-if="loading">加载中...</div>

    <div v-else class="post-list">
      <div v-if="posts.length === 0" class="no-data">
        {{ isSearching ? '没有找到匹配的文章' : '暂无文章，快去写一篇吧！' }}
      </div>

      <div v-else v-for="post in posts" :key="post.id" class="post-card">
        <h2>
          <router-link :to="{ name: 'post-detail', params: { id: post.id }}">
            <span v-html="highlightMatcher(post.title)"></span>
          </router-link>
        </h2>

        <p
          class="excerpt"
          v-html="highlightMatcher(post.content?.substring(0, 100) || '') + '...'"
        ></p>

        <div class="meta">
          <small>📅 {{ new Date(post.created_at).toLocaleDateString() }}</small>
          <span class="category-badge">📂 {{ post.category }}</span>
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
.search-container {
  margin-bottom: 2rem;
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #3aa876;
}

.clear-button {
  background: none;
  border: none;
  color: #666;
  text-decoration: underline;
  cursor: pointer;
}

/* ✅ 新增：针对 v-html 生成的高亮标签进行深度选择 */
:deep(.highlight-keyword) {
  background-color: #f0f8ff;          /* 浅蓝色背景 */
  color: #0066cc;                     /* 深蓝色文字 */
  padding: 2px 6px;                   /* 内边距增加 */
  border-radius: 8px;                 /* 更大的圆角 */
  font-weight: 600;                   /* 稍微加粗 */
  box-shadow:
    0 2px 4px rgba(0, 102, 204, 0.2), /* 下方阴影 */
    inset 0 1px 0 rgba(255, 255, 255, 0.3); /* 上方内阴影增加立体感 */
  border: 1px solid rgba(0, 102, 204, 0.2); /* 细边框 */
  margin: 0 1px;                      /* 微调间距 */
  display: inline-block;              /* 确保边框和阴影正常显示 */
}

.category-badge {
  background-color: #eee;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85em;
  color: #555;
  margin-left: 10px;
}

.tags-container {
  margin-top: 8px;
}

.tag-badge {
  display: inline-block;
  background-color: #e1f5fe; /* 浅蓝 */
  color: #0277bd;
  font-size: 0.8em;
  padding: 2px 8px;
  border-radius: 12px;
  margin-right: 5px;
}

</style>