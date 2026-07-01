<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'

const router = useRouter()
const username = ref('管理员')
const realName = ref('张经理')

onMounted(() => {
  const userInfo = localStorage.getItem('userInfo')
  if (userInfo) {
    const user = JSON.parse(userInfo)
    username.value = user.username || '管理员'
    realName.value = user.real_name || '张经理'
  }
})

const logout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {}
}
</script>

<template>
  <header class="header">
    <div class="header-left">
      <div class="brand-area">
        <span class="brand-name">火锅串串门店</span>
        <span class="brand-divider">|</span>
        <span class="brand-system">竹签计价系统</span>
      </div>
    </div>

    <div class="header-right">
      <div class="user-profile">
        <div class="user-avatar">
          <span>{{ realName.charAt(0) }}</span>
        </div>
        <div class="user-details">
          <span class="user-name">{{ realName }}</span>
          <span class="user-role">门店管理员</span>
        </div>
      </div>

      <el-button @click="logout" class="logout-btn">
        <span>退出</span>
      </el-button>
    </div>
  </header>
</template>

<style scoped lang="scss">
.header {
  height: 64px;
  background: linear-gradient(135deg, #1A1512 0%, #241D19 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  border-bottom: 1px solid rgba(248, 245, 242, 0.08);
  position: relative;

  // 暖色柔光渐变
  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(217, 72, 54, 0.3), transparent);
  }
}

.header-left {
  display: flex;
  align-items: center;

  .brand-area {
    display: flex;
    align-items: center;
    gap: 12px;

    .brand-name {
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 3px;
      background: linear-gradient(to right, #D94836, #E6B87D);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-shadow: 0 0 16px rgba(217, 72, 54, 0.15);
    }

    .brand-divider {
      color: rgba(248, 245, 242, 0.2);
    }

    .brand-system {
      font-size: 13px;
      color: #BFAFA6;
      letter-spacing: 2px;
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 16px 6px 8px;
  background: rgba(248, 245, 242, 0.04);
  border-radius: 9999px;
  border: 1px solid rgba(248, 245, 242, 0.08);
  transition: all 250ms ease;

  &:hover {
    background: rgba(242, 112, 68, 0.08);
    border-color: rgba(242, 112, 68, 0.15);
  }

  .user-avatar {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #D94836, #F27044);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
    color: #fff;
    box-shadow: 0 0 12px rgba(217, 72, 54, 0.25);
  }

  .user-details {
    display: flex;
    flex-direction: column;
    gap: 2px;

    .user-name {
      font-size: 14px;
      font-weight: 500;
      color: #F8F5F2;
    }

    .user-role {
      font-size: 11px;
      color: #BFAFA6;
    }
  }
}

.logout-btn {
  height: 36px;
  padding: 0 16px;
  background: transparent;
  border: 1px solid rgba(248, 245, 242, 0.15);
  border-radius: 9999px;
  color: #BFAFA6;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 250ms ease;
  letter-spacing: 1px;

  &:hover {
    background: rgba(217, 72, 54, 0.1);
    border-color: rgba(217, 72, 54, 0.3);
    color: #F8F5F2;
    box-shadow: 0 0 12px rgba(217, 72, 54, 0.15);
  }
}
</style>