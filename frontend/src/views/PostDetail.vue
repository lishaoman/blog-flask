<script setup>
import { ref, onMounted, computed, nextTick, watch, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/index'
import BackToTop from '../components/BackToTop.vue'

// 引入 Markdown 解析器和清洗器
import { marked } from 'marked'
import DOMPurify from 'dompurify'

// 引入代码高亮库及其样式
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

// 引入 GitHub 风格的 Markdown 样式
import 'github-markdown-css/github-markdown-light.css'

const route = useRoute()
const post = ref(null)
const loading = ref(true)
const error = ref('')

const markdownContainer = ref(null)
const tocContainer = ref(null)

// === 新增：目录相关状态 ===
const tocItems = ref([])
const activeTocId = ref('')

// === 新增：创建自定义渲染器实例 ===
const renderer = new marked.Renderer()

// 重写 heading 方法，为标题添加 id
renderer.heading = function ({ tokens, depth, text, raw }) {
  const level = depth
  const title = raw || text
  if (!title) {
    return `<h${level}>${text}</h${level}>`
  }
  const slug = title.toLowerCase()
    .replace(/[^\w\u4e00-\u9fa5]+/g, '-')
    .replace(/^-|-$/g, '')
  return `<h${level} id="${slug}">${text}</h${level}>`
}

// 配置 marked 使用 highlight.js 和自定义渲染器
marked.setOptions({
  renderer: renderer,
  highlight: function (code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    return hljs.highlight(code, { language }).value
  },
  langPrefix: 'hljs language-',
  gfm: true,
  breaks: false
})

// 计算属性：将 markdown 内容转换为安全的 HTML
const renderedContent = computed(() => {
  if (!post.value || !post.value.content) return ''
  const rawHtml = marked.parse(post.value.content)
  return DOMPurify.sanitize(rawHtml)
})

// === 新增：从渲染后的内容中提取目录 ===
const extractTableOfContents = () => {
  if (!markdownContainer.value) return

  // 查找所有 h2, h3, h4 标题
  const headings = markdownContainer.value.querySelectorAll('h2, h3, h4')

  tocItems.value = Array.from(headings).map((heading, index) => {
    const level = parseInt(heading.tagName.charAt(1))
    const text = heading.textContent
    const id = heading.id

    // 为标题添加 id（如果 renderer 没成功添加）
    if (!id) {
      const slug = text.toLowerCase()
        .replace(/[^\w\u4e00-\u9fa5]+/g, '-')
        .replace(/^-|-$/g, '')
      heading.id = slug
      return { id: slug, text, level, index }
    }

    return { id, text, level, index }
  })
}

// === 新增：点击目录项滚动到对应位置 ===
const scrollToHeading = (id) => {
  const element = document.getElementById(id)
  if (element) {
    // 平滑滚动到目标位置，偏移 20px 以避免被固定导航栏遮挡
    const offset = 80
    const elementPosition = element.getBoundingClientRect().top
    const offsetPosition = elementPosition + window.pageYOffset - offset

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
  }
}

// === 新增：滚动监听，高亮当前目录项 ===
let scrollHandler = null

const setupScrollSpy = () => {
  const headings = markdownContainer.value?.querySelectorAll('h2, h3, h4') || []

  scrollHandler = () => {
    const scrollPosition = window.scrollY + 100 // 偏移量

    let currentHeading = null

    headings.forEach((heading) => {
      const headingPosition = heading.getBoundingClientRect().top + window.pageYOffset
      if (headingPosition <= scrollPosition) {
        currentHeading = heading
      }
    })

    if (currentHeading) {
      activeTocId.value = currentHeading.id
    } else {
      activeTocId.value = ''
    }
  }

  window.addEventListener('scroll', scrollHandler)
}

// 复制代码按钮功能
const addCopyButtons = () => {
  if (!markdownContainer.value) return

  const preBlocks = markdownContainer.value.querySelectorAll('pre')

  preBlocks.forEach((preBlock) => {
    if (preBlock.querySelector('.copy-btn')) return

    const button = document.createElement('button')
    button.className = 'copy-btn'
    button.textContent = '复制代码'

    button.addEventListener('click', async () => {
      const codeElement = preBlock.querySelector('code')
      if (!codeElement) return

      const codeText = codeElement.innerText

      try {
        await navigator.clipboard.writeText(codeText)
        button.textContent = '已复制! ✅'
        button.classList.add('success')

        setTimeout(() => {
          button.textContent = '复制代码'
          button.classList.remove('success')
        }, 2000)
      } catch (err) {
        console.error('复制失败:', err)
        button.textContent = '复制失败 ❌'
      }
    })

    preBlock.appendChild(button)
  })
}

// 监听数据变化
watch(post, async () => {
  if (post.value) {
    await nextTick()
    addCopyButtons()
    extractTableOfContents()
    setupScrollSpy()
  }
})

// 清理滚动监听
onBeforeUnmount(() => {
  if (scrollHandler) {
    window.removeEventListener('scroll', scrollHandler)
  }
})

onMounted(async () => {
  const postId = route.params.id
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

const deletePost = async () => {
  if (!confirm('确定要删除这篇文章吗？此操作不可恢复！😱')) return

  try {
    await api.delete(`/api/posts/${post.value.id}`)
    alert('删除成功 🗑️')
    route.push('/')
  } catch (error) {
    console.error(error)
    alert('删除失败')
  }
}
</script>

<template>
  <div class="post-detail">
    <BackToTop />

    <div v-if="loading" class="loading">⏳ 加载中...</div>

    <div v-else-if="error" class="error">❌ {{ error }}</div>

    <div v-else-if="post" class="content-wrapper">
      <!-- === 新增：文章目录侧边栏 === -->
      <aside v-if="tocItems.length > 0" class="toc-sidebar">
        <div class="toc-header">
          <h3>📑 目录</h3>
        </div>
        <ul class="toc-list">
          <li
            v-for="item in tocItems"
            :key="item.id"
            :class="[
              'toc-item',
              `toc-level-${item.level}`,
              { active: activeTocId === item.id }
            ]"
            @click="scrollToHeading(item.id)"
          >
            {{ item.text }}
          </li>
        </ul>
      </aside>

      <!-- 文章内容区域 -->
      <div class="main-content">
        <div class="content">
          <h1 class="title">{{ post.title }}</h1>
          <div class="meta">
            <span>发布于: {{ new Date(post.created_at).toLocaleString() }}</span>
          </div>
          <div ref="markdownContainer" class="body markdown-body" v-html="renderedContent">
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
    </div>
  </div>
</template>

<style scoped>
.post-detail { max-width: 1400px; margin: 0 auto; }

/* === 新增：布局样式 === */
.content-wrapper {
  display: flex;
  gap: 30px;
  position: relative;
}

.main-content {
  flex: 1;
  min-width: 0; /* 防止内容溢出 */
}

.content {
  max-width: 1600px; /* 800px * 2 = 1600px */
  margin: 0 auto;
}

/* === 新增：目录侧边栏样式 === */
.toc-sidebar {
  position: sticky;
  top: 90px;
  width: 260px;
  flex-shrink: 0;
  max-height: calc(100vh - 110px);
  overflow-y: auto;
  align-self: flex-start;
  border-left: 2px solid #e0e0e0;
  padding-left: 20px;
}

.toc-header {
  border-bottom: 2px solid #42b883;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.toc-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-item {
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  color: #555;
  font-size: 0.9rem;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.toc-item:hover {
  background-color: #f0f0f0;
  color: #2c3e50;
}

/* 不同层级的缩进 */
.toc-level-2 { padding-left: 12px; }
.toc-level-3 { padding-left: 28px; font-size: 0.85rem; }
.toc-level-4 { padding-left: 44px; font-size: 0.8rem; }

/* 激活状态 */
.toc-item.active {
  background-color: #e6f7ff;
  color: #0066cc;
  font-weight: 600;
  border-left: 3px solid #0066cc;
}

/* 原有样式 */
.meta { color: #888; font-size: 0.9em; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
.body p { line-height: 1.6; white-space: pre-wrap; }
.back-btn { display: inline-block; margin-top: 20px; text-decoration: none; color: #42b883; }

/* markdown 样式覆盖 */
.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 100%;
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

/* 代码块样式 */
:deep(.markdown-body pre) {
  background-color: #f6f8fa;
  padding: 16px;
  padding-top: 30px;
  overflow: auto;
  border-radius: 6px;
  position: relative;
}

:deep(.markdown-body code) {
  font-family: 'Courier New', Courier, monospace;
  background-color: rgba(175, 184, 193, 0.2);
  padding: 0.2em 0.4em;
  border-radius: 6px;
}

:deep(.markdown-body pre code) {
  background-color: transparent;
  padding: 0;
}

/* 复制按钮样式 */
:deep(.copy-btn) {
  position: absolute;
  top: 5px;
  right: 5px;
  z-index: 10;
  padding: 4px 10px;
  font-size: 12px;
  color: #555;
  background-color: #eee;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

:deep(.copy-btn:hover) {
  background-color: #e0e0e0;
  color: #333;
}

:deep(.copy-btn.success) {
  background-color: #42b883;
  color: white;
  border-color: #42b883;
}

/* === 新增：响应式设计 - 小屏幕隐藏目录 === */
@media (max-width: 768px) {
  .toc-sidebar {
    display: none;
  }

  .content-wrapper {
    flex-direction: column;
  }
}

/* 平板设备：目录可折叠或简化显示 */
@media (min-width: 769px) and (max-width: 1024px) {
  .toc-sidebar {
    width: 200px;
  }

  .content {
    max-width: 100%;
  }
}
</style>
