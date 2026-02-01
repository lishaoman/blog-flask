<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index'

const tags = ref([])
const loading = ref(true)

// 获取标签列表
const fetchTags = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/tags/')
    tags.value = response.data
  } catch (error) {
    console.error('获取标签列表失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTags()
})
</script>

<template>
  <div class="tag-list">
    <div class="header">
      <h1># 标签列表</h1>
    </div>

    <div v-if="loading">加载中...</div>

    <div v-else>
      <div v-if="tags.length === 0" class="no-data">
        暂无标签
      </div>

      <div v-else class="tag-cloud">
        <router-link
          v-for="tag in tags"
          :key="tag.id"
          :to="{ name: 'tag-posts', params: { id: tag.id } }"
          class="tag-item"
        >
          <span class="tag-name"># {{ tag.name }}</span>
          <span class="post-count">{{ tag.post_count }}</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  text-decoration: none;
  color: #0277bd;
  transition: all 0.2s;
}

.tag-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  background-color: #e1f5fe;
  border-color: #0277bd;
}

.tag-name {
  font-size: 0.95rem;
  font-weight: 500;
}

.post-count {
  background-color: rgba(2, 119, 189, 0.1);
  color: #0277bd;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.no-data {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
