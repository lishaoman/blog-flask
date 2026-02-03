<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import api from '../api/index'
import BackToTop from '../components/BackToTop.vue'

const posts = ref([])
const loading = ref(true)
const isSearching = ref(false) // 是否处于搜索模式
const searchQuery = ref('') // 搜索关键词

// === 新增：分页相关状态 ===
const currentPage = ref(1)
const postsPerPage = ref(10) // 默认每页10条
const totalPosts = ref(0)
const totalPages = ref(0)

// 可选的每页条数选项
const perPageOptions = [5, 10, 15, 20, 30, 50]

// 从 localStorage 读取用户设置的每页条数
const loadPerPage = () => {
  const saved = localStorage.getItem('postsPerPage')
  if (saved) {
    postsPerPage.value = parseInt(saved)
  }
}

// 保存每页条数设置
const savePerPage = (value) => {
  postsPerPage.value = value
  localStorage.setItem('postsPerPage', value.toString())
  currentPage.value = 1 // 切换每页条数时重置到第一页
  fetchPosts()
}

// 获取文章列表（支持分页）
const fetchPosts = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: postsPerPage.value
    }
    const response = await api.get('/api/posts/', { params })
    posts.value = response.data.posts || response.data
    totalPosts.value = response.data.total || posts.value.length
    totalPages.value = response.data.total_pages || Math.ceil(totalPosts.value / postsPerPage.value)
    isSearching.value = false
  } catch (error) {
    console.error('获取列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理函数
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
    // 搜索也支持分页
    const params = {
      q: query,
      page: currentPage.value,
      per_page: postsPerPage.value
    }
    const response = await api.get('/api/posts/search', { params })
    posts.value = response.data.posts || response.data
    totalPosts.value = response.data.total || posts.value.length
    totalPages.value = response.data.total_pages || Math.ceil(totalPosts.value / postsPerPage.value)
  } catch (error) {
    console.error('搜索失败:', error)
    posts.value = []
    totalPosts.value = 0
    totalPages.value = 0
  } finally {
    loading.value = false
  }
}

// === 新增清空函数 ===
const clearSearch = () => {
  searchQuery.value = ''
  currentPage.value = 1
  fetchPosts()
}

// === 新增防抖搜索 (可选) ===
// 当用户输入停止 500ms 后自动触发搜索，无需频繁点击回车
let timer = null
watch(searchQuery, (newVal) => {
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => {
    currentPage.value = 1 // 搜索时重置到第一页
    handleSearch()
  }, 500)
})

// 页码变化时重新获取数据
watch(currentPage, () => {
  if (isSearching.value) {
    handleSearch()
  } else {
    fetchPosts()
  }
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

// 分页操作函数
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const goToPrevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const goToNextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

// 计算当前页显示的起始和结束序号
const displayRange = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage.value + 1
  const end = Math.min(start + postsPerPage.value - 1, totalPosts.value)
  return { start, end }
})

// 计算要显示的页码列表（简化版，显示全部）
const displayPageNumbers = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i++) {
    pages.push(i)
  }
  return pages
})

// 页码跳转输入框
const jumpPage = ref(1)

onMounted(() => {
  loadPerPage()
  fetchPosts()
})
</script>

<template>
  <div class="home">
    <BackToTop />

    <div class="header">
      <h1>📃 最新文章</h1>

      <!-- 新增：每页条数设置 -->
      <div class="per-page-selector">
        <span class="label">每页显示：</span>
        <select v-model="postsPerPage" @change="savePerPage(postsPerPage)" class="per-page-select">
          <option v-for="opt in perPageOptions" :key="opt" :value="opt">
            {{ opt }} 条
          </option>
        </select>
      </div>
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

    <h1>{{ isSearching ? '🔍 搜索结果' : '' }}</h1>

    <!-- 新增：显示总数和分页信息 -->
    <div v-if="!loading && totalPosts > 0" class="pagination-info">
      共 <span class="count">{{ totalPosts }}</span> 篇文章，
      显示第 <span class="count">{{ displayRange.start }}-{{ displayRange.end }}</span> 篇，
      第 <span class="count">{{ currentPage }}</span> / {{ totalPages }} 页
    </div>

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

    <!-- 新增：分页控制栏 -->
    <div v-if="totalPages > 1" class="pagination-bar">
      <div class="pagination-controls">
        <button
          @click="goToPage(1)"
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          首页
        </button>

        <button
          @click="goToPrevPage"
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          上一页
        </button>

        <!-- 页码列表 -->
        <div class="page-numbers">
          <button
            v-for="page in displayPageNumbers"
            :key="page"
            @click="goToPage(page)"
            :class="['page-number', { active: page === currentPage }]"
          >
            {{ page }}
          </button>
        </div>

        <button
          @click="goToNextPage"
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          下一页
        </button>

        <button
          @click="goToPage(totalPages)"
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          末页
        </button>
      </div>

      <!-- 页码跳转 -->
      <div class="page-jump">
        跳转到
        <input
          type="number"
          v-model.number="jumpPage"
          :min="1"
          :max="totalPages"
          class="jump-input"
          @keyup.enter="goToPage(jumpPage)"
        />
        页
        <button @click="goToPage(jumpPage)" class="jump-btn">确定</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  max-width: 1040px; /* 800px * 1.3 = 1040px */
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

/* 每页条数选择器 */
.per-page-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.per-page-select {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
}

.per-page-select:hover {
  border-color: #42b883;
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

/* 分页信息 */
.pagination-info {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #666;
  font-size: 0.9rem;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.pagination-info .count {
  color: #42b883;
  font-weight: bold;
}

/* 分页控制栏 */
.pagination-bar {
  margin-top: 2rem;
  padding: 20px;
  border-top: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.pagination-btn {
  padding: 8px 16px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  color: #555;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #42b883;
  color: white;
  border-color: #42b883;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-number {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  color: #555;
}

.page-number:hover {
  border-color: #42b883;
  color: #42b883;
}

.page-number.active {
  background-color: #42b883;
  color: white;
  border-color: #42b883;
  font-weight: bold;
}

/* 页码跳转 */
.page-jump {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #666;
}

.jump-input {
  width: 60px;
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.jump-btn {
  padding: 6px 12px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.jump-btn:hover {
  background-color: #3aa876;
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

.no-data {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
