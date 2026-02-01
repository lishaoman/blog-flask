<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index'

const categories = ref([])
const loading = ref(true)

// 获取分类列表
const fetchCategories = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/categories/')
    categories.value = response.data
  } catch (error) {
    console.error('获取分类列表失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<template>
  <div class="category-list">
    <div class="header">
      <h1>📂 分类列表</h1>
    </div>

    <div v-if="loading">加载中...</div>

    <div v-else>
      <div v-if="categories.length === 0" class="no-data">
        暂无分类
      </div>

      <div v-else class="category-items">
        <router-link
          v-for="category in categories"
          :key="category.id"
          :to="{ name: 'category-posts', params: { id: category.id } }"
          class="category-item"
        >
          <span class="category-name">{{ category.name }}</span>
          <span class="post-count">{{ category.post_count }} 篇</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }

.category-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  text-decoration: none;
  color: #2c3e50;
  transition: all 0.2s;
}

.category-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-color: #42b883;
}

.category-name {
  font-size: 1.1rem;
  font-weight: 500;
}

.post-count {
  background-color: #f0f0f0;
  color: #666;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
}

.no-data {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
