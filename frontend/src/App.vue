<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">首页</RouterLink> |
      <RouterLink to="/about">关于</RouterLink> |
      <RouterLink to="/categories">📂 分类</RouterLink> |
      <RouterLink to="/tags"># 标签</RouterLink>
      <RouterLink to="/create" class="write-btn">✍️ 写文章</RouterLink>
    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style scoped>
/* 添加一点点基础样式让它看起来不那么简陋 */
header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: #f8f9fa;
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

nav a {
  text-decoration: none;
  color: #42b883;
  font-weight: bold;
  margin: 0 10px;
}

/* 高亮当前激活的链接 */
nav a.router-link-active {
  color: #35495e;
  text-decoration: underline;
}

/* 给写文章按钮加点特殊的样式 */
.write-btn {
  color: #e67e22 !important; /* 橙色高亮 */
}

main {
  padding: 80px 2rem 2rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>