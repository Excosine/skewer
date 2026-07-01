<script setup>
import { ref } from 'vue'
import Sidebar from '@/components/common/Sidebar.vue'
import Header from '@/components/common/Header.vue'

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
}
</script>

<template>
  <div class="admin-layout">
    <Sidebar />
    <div class="main-container">
      <Header :is-dark="isDark" @toggle-theme="toggleTheme" />
      <div class="content-area">
        <router-view />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.admin-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  min-width: 1280px;
  background: #0F0C0A;
  position: relative;
  overflow: hidden;

  // 全局烟火肌理 - 极细微网点纹理
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      radial-gradient(circle at 15% 25%, rgba(217, 72, 54, 0.04) 0%, transparent 40%),
      radial-gradient(circle at 85% 75%, rgba(242, 112, 68, 0.05) 0%, transparent 40%),
      radial-gradient(circle at 50% 50%, rgba(230, 184, 125, 0.03) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
  }
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.content-area {
  flex: 1;
  padding: 32px 28px;
  background: transparent;
  overflow-y: auto;
  position: relative;

  // 内容区暖色柔光光斑
  &::before {
    content: '';
    position: absolute;
    top: 10%;
    right: 15%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(242, 112, 68, 0.06) 0%, transparent 70%);
    pointer-events: none;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: 20%;
    left: 10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(230, 184, 125, 0.04) 0%, transparent 70%);
    pointer-events: none;
  }

  // 自定义滚动条 - 火锅暖色调
  &::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(26, 21, 18, 0.5);
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(217, 72, 54, 0.3);
    border-radius: 4px;
    transition: background 250ms ease;

    &:hover {
      background: rgba(217, 72, 54, 0.5);
    }
  }
}
</style>