<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router' // 用于获取 URL 参数
import api from '../api/index'

// 引入 Markdown 解析器和清洗器
import { marked } from 'marked'
import DOMPurify from 'dompurify'

// 1. 引入代码高亮库及其样式
import hljs from 'highlight.js'
// 你可以选择喜欢的样式，比如 atom-one-dark, github, vs2015 等
import 'highlight.js/styles/github.css'

// 引入 GitHub 风格的 Markdown 样式
import 'github-markdown-css/github-markdown-light.css'

const route = useRoute()
const post = ref(null)
const loading = ref(true)
const error = ref('')

// 创建一个 ref 来引用用来包裹 markdown 内容的 div
const markdownContainer = ref(null)

// 2. 配置 marked 使用 highlight.js
marked.setOptions({
  highlight: function (code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    return hljs.highlight(code, { language }).value
  },
  langPrefix: 'hljs language-' // 必须加上这个前缀，样式才会生效
})

// 计算属性：将 markdown 内容转换为安全的 HTML
const renderedContent = computed(() => {
  if (!post.value || !post.value.content) return ''
  // 1. 解析 Markdown
  const rawHtml = marked.parse(post.value.content)
  // 2. 清洗 HTML (防止 XSS 攻击)
  return DOMPurify.sanitize(rawHtml)
})

// === 核心：添加复制按钮的函数 ===
const addCopyButtons = () => {
  // 确保容器存在
  if (!markdownContainer.value) return

  // 1. 找到所有代码块外层的 <pre> 标签
  const preBlocks = markdownContainer.value.querySelectorAll('pre')

  preBlocks.forEach((preBlock) => {
    // 防止重复添加：如果已经有按钮了，就跳过
    if (preBlock.querySelector('.copy-btn')) return

    // 2. 创建按钮元素
    const button = document.createElement('button')
    button.className = 'copy-btn'
    button.textContent = '复制代码'

    // 3. 添加点击事件
    button.addEventListener('click', async () => {
      // 找到 <pre> 里面的 <code> 标签
      const codeElement = preBlock.querySelector('code')
      if (!codeElement) return

      // 获取纯文本内容
      const codeText = codeElement.innerText

      try {
        // 调用浏览器剪贴板 API
        await navigator.clipboard.writeText(codeText)

        // 复制成功反馈
        button.textContent = '已复制! ✅'
        button.classList.add('success')

        // 2秒后恢复原状
        setTimeout(() => {
          button.textContent = '复制代码'
          button.classList.remove('success')
        }, 2000)
      } catch (err) {
        console.error('复制失败:', err)
        button.textContent = '复制失败 ❌'
      }
    })

    // 4. 将按钮插入到 <pre> 标签内部的最前面
    preBlock.appendChild(button)
  })
}

// === 监听数据变化，触发 DOM 操作 ===
// 当 post 数据加载完成后，等待 DOM 更新完毕，再执行添加按钮的操作
watch(post, async () => {
  if (post.value) {
    // nextTick 确保 v-html 已经完成了 DOM 的渲染
    await nextTick()
    addCopyButtons()
  }
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

/* 确保代码块有背景色和圆角 */
:deep(.markdown-body pre) {
  background-color: #f6f8fa; /* 浅灰色背景 */
  padding: 16px;
  overflow: auto;
  border-radius: 6px;
}

:deep(.markdown-body code) {
  font-family: 'Courier New', Courier, monospace;
  background-color: rgba(175, 184, 193, 0.2);
  padding: 0.2em 0.4em;
  border-radius: 6px;
}

/* 如果是多行代码块，去掉单行代码的背景 */
:deep(.markdown-body pre code) {
  background-color: transparent;
  padding: 0;
}

/* === 代码块和复制按钮样式 === */

/* 1. 设置 pre 为相对定位，作为按钮定位的基准 */
:deep(.markdown-body pre) {
  position: relative;
  padding-top: 30px; /* 顶部留出空间给按钮，防止遮挡代码第一行 */
  background-color: #f6f8fa;
  border-radius: 6px;
}

/* 2. 复制按钮的基本样式 (绝对定位到右上角) */
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

/* 3. 复制成功后的状态样式 */
:deep(.copy-btn.success) {
  background-color: #42b883; /* Vue 绿 */
  color: white;
  border-color: #42b883;
}

</style>