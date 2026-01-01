<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api/index'

const router = useRouter()
const route = useRoute()

const title = ref('')
const content = ref('')
const isSubmitting = ref(false)
const postId = route.params.id

// 进入页面先获取旧数据
onMounted(async () => {
  try {
    const response = await api.get(`/api/posts/${postId}`)
    title.value = response.data.title
    content.value = response.data.content
  } catch (error) {
    alert('无法加载文章数据')
    router.push('/')
  }
})

// 提交更新
const updatePost = async () => {
  isSubmitting.value = true
  try {
    // 发送 PUT 请求
    await api.put(`/api/posts/${postId}`, {
      title: title.value,
      content: content.value
    })
    alert('更新成功！✅')
    router.push(`/post/${postId}`) // 跳转回详情页
  } catch (error) {
    console.error(error)
    alert('更新失败')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="edit-post">
    <h1>✏️ 编辑文章</h1>
    <form @submit.prevent="updatePost">
      <div class="form-group">
        <label>标题</label>
        <input v-model="title" type="text" required>
      </div>
      <div class="form-group">
        <label>内容</label>
        <textarea v-model="content" rows="10" required></textarea>
      </div>
      <div class="actions">
        <button type="submit" :disabled="isSubmitting" class="save-btn">
          {{ isSubmitting ? '保存中...' : '💾 保存修改' }}
        </button>
        <button type="button" @click="router.back()" class="cancel-btn">取消</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* 复用之前的样式，或者简单写一点 */
.edit-post { max-width: 600px; margin: 0 auto; }
.form-group { margin-bottom: 20px; }
input, textarea { width: 100%; padding: 10px; margin-top: 5px; }
.save-btn { background: #35495e; color: white; border: none; padding: 10px 20px; cursor: pointer; margin-right: 10px;}
.cancel-btn { background: #ccc; border: none; padding: 10px 20px; cursor: pointer; }
</style>