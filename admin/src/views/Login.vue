<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, getCaptcha, getCaptchaImageUrl } from '@/api/auth'

const router = useRouter()

const form = ref({ username: 'admin', password: '123456', captcha_code: '' })
const loading = ref(false)
const captchaKey = ref('')
const captchaUrl = ref('')
const captchaLoading = ref(false)

// 粒子动画控制
const particles = ref([])
const particleTimer = ref(null)

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  captcha_code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

const formRef = ref(null)

// 生成粒子
const generateParticles = () => {
  const items = ['🍢', '🔥', '🥩', '🌶️', '🫑', '🧄', '🥬', '🍄', '🧅', '🍖', '🍗', '🥓']
  particles.value = []
  
  for (let i = 0; i < 15; i++) {
    particles.value.push({
      id: i,
      emoji: items[Math.floor(Math.random() * items.length)],
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: 16 + Math.random() * 24,
      duration: 8 + Math.random() * 12,
      delay: Math.random() * 5,
      opacity: 0.08 + Math.random() * 0.12
    })
  }
}

// 获取验证码
const fetchCaptcha = async () => {
  captchaLoading.value = true
  try {
    const res = await getCaptcha()
    captchaKey.value = res.captcha_key
    captchaUrl.value = getCaptchaImageUrl(res.captcha_key)
  } catch {
    ElMessage.error('获取验证码失败')
  } finally {
    captchaLoading.value = false
  }
}

// 刷新验证码
const refreshCaptcha = () => {
  fetchCaptcha()
  form.value.captcha_code = ''
}

const handleLogin = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const res = await login({
        username: form.value.username,
        password: form.value.password,
        captcha_key: captchaKey.value,
        captcha_code: form.value.captcha_code
      })
      localStorage.setItem('token', res.token)
      localStorage.setItem('userInfo', JSON.stringify({
        username: res.username,
        role: res.role,
        real_name: res.real_name
      }))
      ElMessage.success('登录成功')
      router.push('/dashboard')
    } catch (error) {
      // 验证码错误时刷新验证码
      if (error.response?.data?.detail?.includes('验证码')) {
        refreshCaptcha()
      }
    } finally {
      loading.value = false
    }
  })
}

onMounted(() => {
  fetchCaptcha()
  generateParticles()
})

onUnmounted(() => {
  if (particleTimer.value) {
    clearInterval(particleTimer.value)
  }
})
</script>

<template>
  <div class="login-page">
    <!-- 复古烟火背景图片 -->
    <div class="bg-image-layer"></div>
    
    <!-- 深色做旧底色叠加层 -->
    <div class="bg-overlay"></div>
    
    <!-- 烟火氛围光效 - 动态流动 -->
    <div class="ambient-glow">
      <div class="glow-red"></div>
      <div class="glow-orange"></div>
      <div class="glow-gold"></div>
      <div class="glow-warm"></div>
    </div>
    
    <!-- 锅底肌理纹理层 -->
    <div class="texture-layer"></div>
    
    <!-- 火锅粒子动画层 -->
    <div class="particles-layer">
      <div 
        v-for="p in particles" 
        :key="p.id"
        class="particle"
        :style="{
          left: p.x + '%',
          top: p.y + '%',
          fontSize: p.size + 'px',
          animationDuration: p.duration + 's',
          animationDelay: p.delay + 's',
          opacity: p.opacity
        }"
      >
        {{ p.emoji }}
      </div>
    </div>
    
    <!-- 烟雾氤氲效果 -->
    <div class="smoke-layer">
      <div class="smoke smoke-1"></div>
      <div class="smoke smoke-2"></div>
      <div class="smoke smoke-3"></div>
    </div>

    <!-- 登录卡片 - 强化玻璃态悬浮 -->
    <div class="login-card">
      <!-- 卡片边框发光动画 -->
      <div class="card-glow-border"></div>
      <div class="card-glow-border delay"></div>
      
      <!-- 卡片装饰边框 -->
      <div class="card-border-decor"></div>
      
      <!-- 复古装饰图案 -->
      <div class="decor-patterns">
        <div class="pattern pattern-left">🍜</div>
        <div class="pattern pattern-right">🔥</div>
      </div>
      
      <!-- 头部品牌区 - 复古书法风格 -->
      <div class="card-header">
        <div class="brand-info">
          <h1 class="brand-title">火锅串串</h1>
          <div class="title-underline"></div>
          <p class="brand-sub">竹签计价管理员登录入口</p>
        </div>
      </div>

      <!-- 表单区 - 涟漪光晕输入框 -->
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="login-form">
        <el-form-item label="用户名" prop="username">
          <div class="input-wrapper">
            <div class="input-ripple"></div>
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              size="large"
              class="custom-input"
            />
          </div>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <div class="input-wrapper">
            <div class="input-ripple"></div>
            <el-input
              v-model="form.password"
              type="password"
              show-password
              placeholder="请输入密码"
              size="large"
              class="custom-input"
              @keyup.enter="handleLogin"
            />
          </div>
        </el-form-item>

        <!-- 验证码输入框 -->
        <el-form-item label="验证码" prop="captcha_code">
          <div class="captcha-row">
            <div class="input-wrapper captcha-input-wrapper">
              <div class="input-ripple"></div>
              <el-input
                v-model="form.captcha_code"
                placeholder="请输入验证码"
                size="large"
                class="captcha-input"
                maxlength="4"
                @keyup.enter="handleLogin"
              />
            </div>
            <div class="captcha-image-box" @click="refreshCaptcha">
              <img 
                v-if="captchaUrl" 
                :src="captchaUrl" 
                alt="验证码" 
                class="captcha-image"
                :class="{ 'loading': captchaLoading }"
              />
              <div v-if="captchaLoading" class="captcha-loading">
                <span>加载...</span>
              </div>
              <div class="refresh-tip">点击刷新</div>
            </div>
          </div>
        </el-form-item>

        <!-- 复古红底登录按钮 -->
        <el-button
          type="primary"
          :loading="loading"
          block
          size="large"
          @click="handleLogin"
          class="retro-btn"
        >
          <span v-if="!loading">进入系统</span>
          <span v-else>正在登录...</span>
        </el-button>
      </el-form>

      <!-- 底部提示 - 复古小标签 -->
      <div class="card-footer">
        <div class="retro-tag">
          <span class="tag-text">默认账号: admin / 123456</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-page {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

// 复古烟火背景图片
.bg-image-layer {
  position: absolute;
  inset: 0;
  background-image: url('@/assets/images/login-bg.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.35;
  z-index: 0;
}

// 深色做旧底色叠加层
.bg-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, 
    rgba(15, 10, 8, 0.7) 0%, 
    rgba(26, 18, 14, 0.6) 30%, 
    rgba(38, 28, 22, 0.5) 70%, 
    rgba(15, 10, 8, 0.75) 100%
  );
  z-index: 1;
}

// 烟火氛围光效 - 动态流动
.ambient-glow {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;

  .glow-red {
    position: absolute;
    top: 10%;
    left: 15%;
    width: 450px;
    height: 450px;
    background: radial-gradient(circle, rgba(139, 35, 25, 0.3) 0%, transparent 70%);
    filter: blur(70px);
    animation: flow-red 12s ease-in-out infinite;
  }

  .glow-orange {
    position: absolute;
    bottom: 15%;
    right: 10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(180, 80, 50, 0.25) 0%, transparent 70%);
    filter: blur(60px);
    animation: flow-orange 15s ease-in-out infinite reverse;
  }

  .glow-gold {
    position: absolute;
    top: 40%;
    left: 40%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(230, 184, 125, 0.18) 0%, transparent 70%);
    filter: blur(50px);
    animation: flow-gold 10s ease-in-out infinite;
  }

  .glow-warm {
    position: absolute;
    top: 60%;
    left: 60%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(200, 120, 80, 0.2) 0%, transparent 70%);
    filter: blur(55px);
    animation: flow-warm 14s ease-in-out infinite reverse;
  }
}

// 锅底肌理纹理层
.texture-layer {
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
  opacity: 0.25;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(60, 40, 30, 0.1) 0%, transparent 35%),
    radial-gradient(circle at 80% 70%, rgba(50, 35, 25, 0.08) 0%, transparent 35%),
    radial-gradient(circle at 50% 50%, rgba(70, 45, 35, 0.06) 0%, transparent 45%);
}

// 火锅粒子动画层
.particles-layer {
  position: absolute;
  inset: 0;
  z-index: 4;
  pointer-events: none;
  overflow: hidden;

  .particle {
    position: absolute;
    animation: float-particle linear infinite;
    filter: blur(0.5px);
  }
}

// 烟雾氤氲效果
.smoke-layer {
  position: absolute;
  inset: 0;
  z-index: 5;
  pointer-events: none;

  .smoke {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(180, 80, 50, 0.05) 0%, transparent 70%);
    filter: blur(30px);
    animation: smoke-float 20s ease-in-out infinite;
  }

  .smoke-1 {
    top: 20%;
    left: 30%;
    width: 200px;
    height: 200px;
    animation-delay: 0s;
  }

  .smoke-2 {
    top: 40%;
    right: 25%;
    width: 180px;
    height: 180px;
    animation-delay: -7s;
  }

  .smoke-3 {
    bottom: 30%;
    left: 45%;
    width: 220px;
    height: 220px;
    animation-delay: -14s;
  }
}

@keyframes float-particle {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  100% {
    transform: translateY(-100vh) rotate(360deg);
  }
}

@keyframes flow-red {
  0%, 100% { 
    opacity: 0.5; 
    transform: translate(0, 0) scale(1); 
  }
  50% { 
    opacity: 0.7; 
    transform: translate(30px, -20px) scale(1.1); 
  }
}

@keyframes flow-orange {
  0%, 100% { 
    opacity: 0.4; 
    transform: translate(0, 0) scale(1); 
  }
  50% { 
    opacity: 0.6; 
    transform: translate(-40px, 30px) scale(1.15); 
  }
}

@keyframes flow-gold {
  0%, 100% { 
    opacity: 0.3; 
    transform: translate(-50%, -50%) scale(1); 
  }
  50% { 
    opacity: 0.5; 
    transform: translate(-50%, -50%) scale(1.2); 
  }
}

@keyframes flow-warm {
  0%, 100% { 
    opacity: 0.35; 
    transform: translate(0, 0) scale(1); 
  }
  50% { 
    opacity: 0.55; 
    transform: translate(25px, -25px) scale(1.1); 
  }
}

@keyframes smoke-float {
  0%, 100% {
    opacity: 0.3;
    transform: translateY(0) scale(1);
  }
  50% {
    opacity: 0.5;
    transform: translateY(-30px) scale(1.2);
  }
}

// 登录卡片 - 强化玻璃态悬浮
.login-card {
  width: 440px;
  padding: 48px 44px;
  
  // 强化玻璃态效果
  background: linear-gradient(145deg, 
    rgba(40, 30, 24, 0.95) 0%, 
    rgba(32, 24, 18, 0.92) 50%, 
    rgba(28, 20, 14, 0.98) 100%
  );
  backdrop-filter: blur(20px);  // 强化模糊
  -webkit-backdrop-filter: blur(20px);
  
  border-radius: 24px;
  position: relative;
  z-index: 10;
  
  // 强化边框发光
  border: 1.5px solid rgba(180, 80, 50, 0.18);
  
  // 多层柔光外发光
  box-shadow:
    0 25px 80px rgba(15, 10, 8, 0.6),
    0 0 50px rgba(180, 80, 50, 0.12),
    0 0 100px rgba(139, 35, 25, 0.08),
    inset 0 2px 0 rgba(200, 150, 100, 0.1),
    inset 0 -2px 0 rgba(139, 35, 25, 0.08);

  // 卡片边框发光动画
  .card-glow-border {
    position: absolute;
    inset: -2px;
    border-radius: 26px;
    border: 2px solid transparent;
    background: linear-gradient(90deg, 
      transparent, 
      rgba(180, 80, 50, 0.3), 
      rgba(230, 184, 125, 0.25), 
      rgba(139, 35, 25, 0.35), 
      transparent
    ) border-box;
    mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
    -webkit-mask-composite: xor;
    animation: glow-rotate 8s linear infinite;
    pointer-events: none;

    &.delay {
      animation-delay: -4s;
      opacity: 0.6;
    }
  }

  // 卡片装饰边框
  .card-border-decor {
    position: absolute;
    top: -2px;
    left: 12%;
    right: 12%;
    height: 3px;
    background: linear-gradient(to right, 
      transparent, 
      rgba(180, 80, 50, 0.6), 
      rgba(139, 35, 25, 0.7), 
      rgba(230, 184, 125, 0.5), 
      rgba(180, 80, 50, 0.6), 
      transparent
    );
    box-shadow: 0 0 10px rgba(180, 80, 50, 0.35);
  }

  // 复古装饰图案
  .decor-patterns {
    position: absolute;
    top: 20px;
    width: 100%;
    height: 100%;
    pointer-events: none;

    .pattern {
      position: absolute;
      font-size: 28px;
      opacity: 0.15;
      filter: blur(1px);
    }

    .pattern-left {
      left: 15px;
      animation: decor-float 6s ease-in-out infinite;
    }

    .pattern-right {
      right: 15px;
      animation: decor-float 6s ease-in-out infinite reverse;
    }
  }
}

@keyframes glow-rotate {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 200% 50%;
  }
}

@keyframes decor-float {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.15;
  }
  50% {
    transform: translateY(-8px);
    opacity: 0.22;
  }
}

// 头部品牌区 - 复古书法风格
.card-header {
  text-align: center;
  margin-bottom: 42px;

  .brand-info {
    .brand-title {
      font-size: 40px;
      font-weight: 900;
      margin: 0 0 16px 0;
      letter-spacing: 14px;
      font-family: 
        'STXingkai', '华文行楷',
        'FZXingkai-S11', '方正行楷',
        'STKaiti', 'KaiTi', '楷体',
        'LiSu', '隶书',
        serif;
      
      background: linear-gradient(135deg, 
        #B06040 0%, 
        #D08050 20%, 
        #E09060 40%, 
        #C07040 60%, 
        #D08050 80%, 
        #A05030 100%
      );
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      
      filter: 
        drop-shadow(0 0 25px rgba(180, 80, 50, 0.5))
        drop-shadow(0 3px 6px rgba(15, 10, 8, 0.4));
      
      position: relative;
      animation: title-glow 3s ease-in-out infinite;
      
      &::before,
      &::after {
        content: '◆';
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        font-size: 16px;
        color: rgba(230, 184, 125, 0.6);
        -webkit-text-fill-color: rgba(230, 184, 125, 0.6);
        filter: none;
        animation: decor-pulse 2s ease-in-out infinite;
      }
      
      &::before { left: -32px; animation-delay: 0s; }
      &::after { right: -32px; animation-delay: -1s; }
    }

    .title-underline {
      width: 120px;
      height: 2.5px;
      margin: 0 auto 18px;
      background: linear-gradient(to right, 
        transparent, 
        rgba(180, 80, 50, 0.7), 
        rgba(230, 184, 125, 0.6), 
        rgba(139, 35, 25, 0.8), 
        rgba(230, 184, 125, 0.6), 
        rgba(180, 80, 50, 0.7), 
        transparent
      );
      box-shadow: 0 0 8px rgba(180, 80, 50, 0.35);
      animation: underline-glow 4s ease-in-out infinite;
    }

    .brand-sub {
      font-size: 18px;  // 字体增大
      color: #C8B8A8;
      margin: 0;
      letter-spacing: 6px;
      font-weight: 400;
      font-family: 'STKaiti', 'KaiTi', '楷体', serif;
    }
  }
}

@keyframes title-glow {
  0%, 100% {
    filter: 
      drop-shadow(0 0 25px rgba(180, 80, 50, 0.5))
      drop-shadow(0 3px 6px rgba(15, 10, 8, 0.4));
  }
  50% {
    filter: 
      drop-shadow(0 0 35px rgba(180, 80, 50, 0.6))
      drop-shadow(0 4px 8px rgba(15, 10, 8, 0.5));
  }
}

@keyframes decor-pulse {
  0%, 100% {
    opacity: 0.6;
    transform: translateY(-50%) scale(1);
  }
  50% {
    opacity: 0.8;
    transform: translateY(-50%) scale(1.1);
  }
}

@keyframes underline-glow {
  0%, 100% {
    box-shadow: 0 0 8px rgba(180, 80, 50, 0.35);
    opacity: 1;
  }
  50% {
    box-shadow: 0 0 12px rgba(230, 184, 125, 0.4);
    opacity: 0.9;
  }
}

// 表单区 - 涟漪光晕输入框
.login-form {
  .el-form-item {
    margin-bottom: 30px;

    :deep(.el-form-item__label) {
      color: #C8B8A8;
      font-weight: 500;
      font-size: 14px;
      letter-spacing: 3px;
      padding-bottom: 12px;
      
      &::before {
        color: rgba(230, 184, 125, 0.9);
      }
    }

    // 输入框包装器 - 涟漪效果
    .input-wrapper {
      position: relative;
      
      // 涟漪光晕层
      .input-ripple {
        position: absolute;
        inset: -4px;
        border-radius: 14px;
        background: radial-gradient(circle at center, 
          rgba(180, 80, 50, 0.08) 0%, 
          transparent 70%
        );
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
        z-index: 0;
      }
      
      &:focus-within .input-ripple {
        opacity: 1;
        animation: ripple-expand 1.5s ease-out infinite;
      }
    }

    :deep(.el-input__wrapper) {
      background: rgba(35, 28, 22, 0.75);
      border: 1.5px solid rgba(139, 35, 25, 0.25);
      border-radius: 12px;
      box-shadow: 
        0 2px 8px rgba(15, 10, 8, 0.15),
        inset 0 1px 0 rgba(200, 150, 100, 0.05);
      padding: 16px 20px;
      transition: all 350ms ease;
      position: relative;
      z-index: 1;

      &:hover {
        border-color: rgba(180, 80, 50, 0.35);
        background: rgba(40, 32, 26, 0.8);
        box-shadow: 
          0 4px 12px rgba(15, 10, 8, 0.2),
          inset 0 1px 0 rgba(200, 150, 100, 0.08);
      }

      &.is-focus {
        border-color: rgba(230, 184, 125, 0.5);
        box-shadow: 
          0 0 25px rgba(180, 80, 50, 0.2),
          0 0 50px rgba(230, 184, 125, 0.08),
          inset 0 0 12px rgba(180, 80, 50, 0.08);
        background: rgba(45, 36, 28, 0.85);
      }
    }

    :deep(.el-input__inner) {
      color: #E0D0C0;
      font-size: 15px;
      letter-spacing: 1.5px;

      &::placeholder {
        color: #9A8A7A;
      }
    }
  }
}

@keyframes ripple-expand {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.15);
    opacity: 0;
  }
}

// 验证码行样式
.captcha-row {
  display: flex;
  gap: 14px;
  align-items: stretch;

  .captcha-input-wrapper {
    flex: 1;
    
    .input-ripple {
      inset: -3px;
    }
  }

  .captcha-input {
    :deep(.el-input__wrapper) {
      background: rgba(35, 28, 22, 0.75);
      border: 1.5px solid rgba(139, 35, 25, 0.25);
      border-radius: 12px;
      box-shadow: 
        0 2px 8px rgba(15, 10, 8, 0.15),
        inset 0 1px 0 rgba(200, 150, 100, 0.05);
      padding: 16px 20px;
      transition: all 350ms ease;

      &:hover {
        border-color: rgba(180, 80, 50, 0.35);
        background: rgba(40, 32, 26, 0.8);
      }

      &.is-focus {
        border-color: rgba(230, 184, 125, 0.5);
        box-shadow: 
          0 0 25px rgba(180, 80, 50, 0.2),
          0 0 50px rgba(230, 184, 125, 0.08),
          inset 0 0 12px rgba(180, 80, 50, 0.08);
        background: rgba(45, 36, 28, 0.85);
      }
    }

    :deep(.el-input__inner) {
      color: #E0D0C0;
      font-size: 15px;
      letter-spacing: 3px;
      font-weight: 600;
      text-transform: uppercase;

      &::placeholder {
        color: #9A8A7A;
      }
    }
  }

  .captcha-image-box {
    width: 130px;
    height: 52px;
    position: relative;
    cursor: pointer;
    border-radius: 12px;
    overflow: hidden;
    
    border: 1.5px solid rgba(139, 35, 25, 0.25);
    
    box-shadow: 
      0 3px 10px rgba(15, 10, 8, 0.2),
      inset 0 1px 0 rgba(200, 150, 100, 0.06);
    
    transition: all 300ms ease;

    &:hover {
      border-color: rgba(180, 80, 50, 0.4);
      box-shadow: 
        0 6px 16px rgba(15, 10, 8, 0.28),
        0 0 20px rgba(180, 80, 50, 0.1),
        inset 0 1px 0 rgba(200, 150, 100, 0.1);
      transform: scale(1.03);
    }

    .captcha-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      
      &.loading {
        opacity: 0.3;
      }
    }

    .captcha-loading {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(45, 40, 35, 0.92);
      
      span {
        font-size: 13px;
        color: #B8A898;
        letter-spacing: 2px;
      }
    }

    .refresh-tip {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 4px 0;
      background: rgba(15, 10, 8, 0.75);
      text-align: center;
      
      font-size: 12px;
      color: rgba(180, 80, 50, 0.8);
      letter-spacing: 2px;
      
      opacity: 0;
      transition: opacity 300ms ease;
    }

    &:hover .refresh-tip {
      opacity: 1;
    }
  }
}

// 复古红底登录按钮 - 强化效果
.retro-btn {
  height: 56px;
  margin-top: 16px;
  
  background: linear-gradient(135deg, 
    #8B3525 0%, 
    #A04030 25%, 
    #B05040 50%, 
    #C06050 75%, 
    #903020 100%
  );
  border: none;
  border-radius: 16px;
  
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 8px;
  color: #F8E8D8;
  
  font-family: 
    'STXingkai', '华文行楷',
    'STKaiti', 'KaiTi', '楷体',
    serif;
  
  box-shadow: 
    0 12px 35px rgba(139, 35, 25, 0.4),
    0 0 45px rgba(180, 80, 50, 0.15),
    0 0 80px rgba(230, 184, 125, 0.08),
    inset 0 2px 0 rgba(200, 150, 100, 0.15),
    inset 0 -2px 0 rgba(139, 35, 25, 0.1);
  
  transition: all 350ms ease;
  position: relative;
  
  // 按钮内部光晕动画
  &::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    background: linear-gradient(90deg, 
      transparent, 
      rgba(230, 184, 125, 0.08), 
      transparent
    );
    animation: btn-glow 3s linear infinite;
    pointer-events: none;
  }

  &:hover {
    background: linear-gradient(135deg, 
      #A04030 0%, 
      #B05040 25%, 
      #C06050 50%, 
      #D07060 75%, 
      #A04030 100%
    );
    box-shadow: 
      0 16px 45px rgba(139, 35, 25, 0.5),
      0 0 60px rgba(180, 80, 50, 0.2),
      0 0 100px rgba(230, 184, 125, 0.12),
      inset 0 2px 0 rgba(200, 150, 100, 0.2);
    transform: scale(1.04) translateY(-2px);
  }

  &:active {
    transform: scale(0.98) translateY(1px);
    box-shadow: 
      0 8px 22px rgba(139, 35, 25, 0.35),
      0 0 30px rgba(180, 80, 50, 0.12);
  }
}

@keyframes btn-glow {
  0% {
    background-position: -100% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

// 底部提示 - 复古小标签
.card-footer {
  text-align: center;
  margin-top: 36px;
  padding-top: 32px;
  border-top: 1.5px solid rgba(139, 35, 25, 0.18);

  .retro-tag {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 16px 32px;
    
    background: rgba(35, 28, 22, 0.6);
    border: 1.5px solid rgba(139, 35, 25, 0.25);
    border-radius: 12px;
    
    box-shadow: 
      0 0 10px rgba(180, 80, 50, 0.05),
      inset 0 1px 0 rgba(200, 150, 100, 0.06);
    
    .tag-text {
      font-size: 15px;
      color: #C8B8A8;
      letter-spacing: 5px;
      font-weight: 400;
      font-family: 'STKaiti', 'KaiTi', '楷体', serif;
    }
  }
}
</style>