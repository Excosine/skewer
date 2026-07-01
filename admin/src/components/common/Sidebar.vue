<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const menuItems = [
  { path: '/dashboard', title: '仪表盘' },
  { path: '/monitor', title: '运营监控' },
  { path: '/users', title: '员工管理' },
  { path: '/prices', title: '价格管理' },
  { path: '/reports', title: '数据报表' },
  { path: '/logs', title: '操作日志' }
]

const activeIndex = ref(route.path)

const handleSelect = (path) => {
  activeIndex.value = path
  router.push(path)
}
</script>

<template>
  <aside class="sidebar">
    <!-- 品牌 Logo - 立体鎏金效果 -->
    <div class="sidebar-brand">
      <div class="brand-glow"></div>
      <div class="brand-info">
        <span class="brand-title">火锅串串</span>
        <span class="brand-sub">竹签计价系统</span>
      </div>
    </div>

    <!-- 导航菜单 -->
    <el-menu :default-active="activeIndex" @select="handleSelect" class="sidebar-menu">
      <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
        <span class="menu-text">{{ item.title }}</span>
      </el-menu-item>
    </el-menu>

    <!-- 底部状态 - 立体效果 -->
    <div class="sidebar-footer">
      <div class="status-container">
        <div class="status-glow"></div>
        <span class="status-text">火热经营中</span>
      </div>
    </div>
  </aside>
</template>

<style scoped lang="scss">
.sidebar {
  width: 240px;
  height: 100vh;
  background: linear-gradient(180deg, #0F0C0A 0%, #1A1512 50%, #241D19 100%);
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(248, 245, 242, 0.08);
  position: relative;
  overflow: hidden;
  box-shadow: 4px 0 24px rgba(15, 12, 10, 0.5);

  // 背景暖色光斑 - 增加立体感
  &::before {
    content: '';
    position: absolute;
    top: 15%;
    left: 50%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(217, 72, 54, 0.12) 0%, transparent 70%);
    transform: translateX(-50%);
    pointer-events: none;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: 30%;
    right: -50px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(230, 184, 125, 0.08) 0%, transparent 70%);
    pointer-events: none;
  }
}

// 品牌区域 - 立体鎏金效果
.sidebar-brand {
  padding: 36px 24px 28px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(248, 245, 242, 0.08);
  position: relative;
  background: linear-gradient(180deg, rgba(217, 72, 54, 0.05) 0%, transparent 100%);

  // 顶部鎏金光晕装饰
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 24px;
    right: 24px;
    height: 2px;
    background: linear-gradient(to right, transparent, rgba(230, 184, 125, 0.4), transparent);
    box-shadow: 0 0 12px rgba(230, 184, 125, 0.3);
  }

  .brand-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 180px;
    height: 80px;
    background: radial-gradient(ellipse, rgba(230, 184, 125, 0.15) 0%, transparent 70%);
    pointer-events: none;
  }

  .brand-info {
    flex: 1;
    text-align: center;
    position: relative;

    .brand-title {
      font-size: 22px;
      font-weight: 700;
      color: #E6B87D;
      letter-spacing: 5px;
      display: block;
      text-shadow:
        0 0 24px rgba(230, 184, 125, 0.5),
        0 2px 4px rgba(15, 12, 10, 0.3);
      background: linear-gradient(135deg, #E6B87D 0%, #F27044 50%, #D94836 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      position: relative;

      // 标题下方鎏金装饰线
      &::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 2px;
        background: linear-gradient(to right, transparent, #E6B87D, transparent);
        box-shadow: 0 0 8px rgba(230, 184, 125, 0.4);
      }
    }

    .brand-sub {
      font-size: 13px;
      color: #BFAFA6;
      letter-spacing: 3px;
      display: block;
      margin-top: 16px;
    }
  }
}

// 菜单样式 - 立体悬浮效果
.sidebar-menu {
  flex: 1;
  background: transparent;
  border-right: none;
  padding: 16px 0;
  overflow-y: auto;

  .el-menu-item {
    height: 52px;
    line-height: 52px;
    margin: 6px 16px;
    padding-left: 24px !important;
    border-radius: 12px;
    color: #BFAFA6;
    background: rgba(26, 21, 18, 0.3);
    border: 1px solid transparent;
    transition: all 300ms ease;
    display: flex;
    align-items: center;
    position: relative;
    box-shadow: 0 2px 8px rgba(15, 12, 10, 0.2);

    .menu-text {
      font-size: 15px;
      font-weight: 500;
      letter-spacing: 3px;
    }

    &:hover {
      background: rgba(242, 112, 68, 0.12);
      border-color: rgba(242, 112, 68, 0.25);
      color: #F8F5F2;
      transform: translateX(4px);
      box-shadow:
        0 4px 16px rgba(242, 112, 68, 0.15),
        2px 0 8px rgba(242, 112, 68, 0.1);
    }

    &.is-active {
      background: linear-gradient(135deg, rgba(217, 72, 54, 0.2), rgba(242, 112, 68, 0.15));
      border-color: rgba(217, 72, 54, 0.4);
      color: #F8F5F2;
      box-shadow:
        0 4px 20px rgba(217, 72, 54, 0.2),
        2px 0 12px rgba(217, 72, 54, 0.15),
        inset 0 1px 0 rgba(248, 245, 242, 0.05);
      position: relative;
      transform: translateX(6px);

      // 左侧牛油红高亮条 - 立体发光效果
      &::before {
        content: '';
        position: absolute;
        left: -2px;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 32px;
        background: linear-gradient(180deg, #E6B87D, #D94836, #F27044);
        border-radius: 2px;
        box-shadow:
          0 0 16px rgba(217, 72, 54, 0.5),
          0 0 8px rgba(230, 184, 125, 0.3);
      }

      // 右侧内阴影增加立体感
      &::after {
        content: '';
        position: absolute;
        right: 0;
        top: 0;
        bottom: 0;
        width: 1px;
        background: linear-gradient(180deg, transparent, rgba(230, 184, 125, 0.2), transparent);
      }
    }
  }
}

// 底部状态 - 立体效果
.sidebar-footer {
  padding: 20px 16px 24px;
  border-top: 1px solid rgba(248, 245, 242, 0.08);
  background: linear-gradient(180deg, transparent 0%, rgba(217, 72, 54, 0.03) 100%);
  position: relative;

  // 底部鎏金装饰
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 24px;
    right: 24px;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(230, 184, 125, 0.2), transparent);
  }

  .status-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 12px 20px;
    background: rgba(26, 21, 18, 0.4);
    border: 1px solid rgba(217, 72, 54, 0.15);
    border-radius: 12px;
    box-shadow:
      0 4px 16px rgba(217, 72, 54, 0.1),
      inset 0 1px 0 rgba(248, 245, 242, 0.03);
    position: relative;

    // 容器内部光晕
    &::before {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at center, rgba(217, 72, 54, 0.05) 0%, transparent 70%);
      border-radius: 12px;
    }

    .status-glow {
      width: 10px;
      height: 10px;
      background: linear-gradient(135deg, #D94836, #F27044);
      border-radius: 50%;
      box-shadow:
        0 0 16px rgba(217, 72, 54, 0.6),
        0 0 8px rgba(230, 184, 125, 0.3);
      animation: pulse-glow 2s ease-in-out infinite;
    }

    .status-text {
      font-size: 14px;
      color: #E6B87D;
      letter-spacing: 3px;
      font-weight: 600;
      text-shadow: 0 0 8px rgba(230, 184, 125, 0.3);
    }
  }
}

@keyframes pulse-glow {
  0%, 100% {
    opacity: 1;
    box-shadow:
      0 0 16px rgba(217, 72, 54, 0.6),
      0 0 8px rgba(230, 184, 125, 0.3);
  }
  50% {
    opacity: 0.7;
    box-shadow:
      0 0 12px rgba(217, 72, 54, 0.4),
      0 0 6px rgba(230, 184, 125, 0.2);
  }
}
</style>