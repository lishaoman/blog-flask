<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/index'

const router = useRouter()

// 定义表单数据
const title = ref('')
const content = ref('')
const isSubmitting = ref(false)

// 提交表单
const submitPost = async () => {
  // 简单的非空校验
  if (!title.value.trim() || !content.value.trim()) {
    alert('标题和内容不能为空！')
    return
  }

  isSubmitting.value = true

  try {
    // 发送 POST 请求到后端
    await api.post('/api/posts/', {
      title: title.value,
      content: content.value
    })

    // 成功后，跳转回首页
    alert('发布成功！🎉')
    router.push('/')

  } catch (error) {
    console.error(error)
    alert('发布失败，请检查网络或后端服务。')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="create-post">
    <h1>✍️ 写新文章</h1>

    <form @submit.prevent="submitPost">
      <div class="form-group">
        <label for="title">标题</label>
        <input
          id="title"
          v-model="title"
          type="text"
          placeholder="请输入文章标题..."
          required
        >
      </div>

      <div class="form-group">
        <label for="content">内容</label>
        <textarea
          id="content"
          v-model="content"
          rows="10"
          placeholder="既然来了，就写点什么吧..."
          required
        ></textarea>
      </div>

      <div class="actions">
        <button type="submit" :disabled="isSubmitting" class="submit-btn">
          {{ isSubmitting ? '发布中...' : '🚀 发布文章' }}
        </button>
        <router-link to="/" class="cancel-btn">取消</router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>
.create-post { max-width: 600px; margin: 0 auto; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: bold; }
.form-group input, .form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}
.form-group textarea { resize: vertical; }
.submit-btn {
  background-color: #42b883;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-right: 10px;
}
.submit-btn:disabled { background-color: #a8d5c2; cursor: not-allowed; }
.cancel-btn { text-decoration: none; color: #666; }
</style>