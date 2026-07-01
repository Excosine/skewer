<template>
  <div class="login-root">
    <!-- Background layers -->
    <div class="bg-layer">
      <div class="bg-charcoal" />
      <div class="bg-glow-top-right" />
      <div class="bg-glow-bottom-left" />
      <div class="bg-glow-center" />
      <div class="bg-food-pattern" />
      <div class="bg-noise" />
    </div>

    <div class="login-container">
      <div class="login-card">
        <!-- Animated flame border -->
        <div class="card-border" />

        <!-- Card content -->
        <div class="card-content">
          <!-- Logo -->
          <div class="logo-wrap">
            <div class="logo-box">
              <svg class="logo-flame" viewBox="0 0 40 40" fill="none">
                <path d="M20 4C16 12 10 16 10 22C10 27.5228 14.4772 32 20 32C25.5228 32 30 27.5228 30 22C30 16 24 12 20 4Z" fill="url(#flameGrad)" />
                <path d="M20 12C18 16 15 18 15 21.5C15 24.5376 17.4624 27 20.5 27C23.5376 27 26 24.5376 26 21.5C26 18 22 16 20 12Z" fill="url(#flameInner)" />
                <defs>
                  <linearGradient id="flameGrad" x1="20" y1="4" x2="20" y2="32">
                    <stop offset="0%" stop-color="#FFD700" />
                    <stop offset="40%" stop-color="#FF8C42" />
                    <stop offset="100%" stop-color="#FF4A22" />
                  </linearGradient>
                  <linearGradient id="flameInner" x1="20" y1="12" x2="20" y2="27">
                    <stop offset="0%" stop-color="#FFF5E0" />
                    <stop offset="50%" stop-color="#FFB347" />
                    <stop offset="100%" stop-color="#FF6B35" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <h1 class="login-title">签子计数</h1>
            <p class="login-subtitle">服务员端</p>
          </div>

          <!-- Form -->
          <form @submit.prevent="submit" class="login-form">
            <div v-if="error" class="form-error">{{ error }}</div>

            <div class="field">
              <label class="field-label">用户名</label>
              <div class="input-wrap">
                <svg class="input-icon" viewBox="0 0 20 20" fill="none">
                  <circle cx="10" cy="7" r="4" stroke="currentColor" stroke-width="1.5" />
                  <path d="M3 18C3 14.6863 6.13401 12 10 12C13.866 12 17 14.6863 17 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                </svg>
                <input v-model="username" type="text" required autofocus
                  placeholder="请输入用户名" />
              </div>
            </div>

            <div class="field">
              <label class="field-label">密码</label>
              <div class="input-wrap">
                <svg class="input-icon" viewBox="0 0 20 20" fill="none">
                  <rect x="3" y="9" width="14" height="9" rx="2" stroke="currentColor" stroke-width="1.5" />
                  <path d="M7 9V6C7 4.34315 8.34315 3 10 3C11.6569 3 13 4.34315 13 6V9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                </svg>
                <input v-model="password" :type="showPw ? 'text' : 'password'" required
                  placeholder="请输入密码" />
                <button type="button" class="pw-toggle" @click="showPw = !showPw" tabindex="-1">
                  <svg v-if="!showPw" viewBox="0 0 20 20" fill="none">
                    <path d="M10 4C5 4 2 10 2 10C2 10 5 16 10 16C15 16 18 10 18 10C18 10 15 4 10 4Z" stroke="currentColor" stroke-width="1.5" />
                    <circle cx="10" cy="10" r="3" stroke="currentColor" stroke-width="1.5" />
                  </svg>
                  <svg v-else viewBox="0 0 20 20" fill="none">
                    <path d="M4 4L16 16M12.5 8.5C12.5 7.11929 11.3807 6 10 6C8.61929 6 7.5 7.11929 7.5 8.5M7.5 8.5V11.5M7.5 8.5L4.5 5.5M16.5 10.5C16.5 10.5 14 15 10 15C8.5 15 7.2 14.2 6.3 13.2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                    <path d="M2 10C2 10 5 4 10 4C12 4 13.7 5 15 6.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="field">
              <label class="field-label">验证码</label>
              <div class="captcha-row">
                <div class="input-wrap captcha-input">
                  <input v-model="captchaInput" type="text" required maxlength="4"
                    placeholder="输入验证码" />
                </div>
                <img v-if="captchaUrl" :src="captchaUrl" @click="refreshCaptcha"
                  alt="验证码" class="captcha-canvas" />
              </div>
            </div>

            <button type="submit" :disabled="loading" class="login-btn">
              <span v-if="!loading">登 录</span>
              <span v-else class="btn-loading">
                <span class="spinner" />
                登录中...
              </span>
            </button>
          </form>

          <!-- Default accounts -->
          <div class="default-accounts">
            <p class="accounts-label">默认账号</p>
            <div class="accounts-list">
              <span class="account-item">admin / 123456 张经理</span>
              <span class="account-divider" />
              <span class="account-item">waiter01 / 123456 小李</span>
            </div>
          </div>
        </div>
      </div>


    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { api } from "../api";

const router = useRouter();
const auth = useAuthStore();
const username = ref("");
const password = ref("");
const showPw = ref(false);
const captchaInput = ref("");
const captchaKey = ref("");
const captchaUrl = ref("");
const error = ref("");
const loading = ref(false);

async function fetchCaptcha() {
  try {
    const data = await api.getCaptcha();
    captchaKey.value = data.captcha_key;
    captchaUrl.value = api.getCaptchaImageUrl(data.captcha_key);
  } catch {
    error.value = "获取验证码失败";
  }
}

function refreshCaptcha() {
  captchaInput.value = "";
  fetchCaptcha();
}

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await auth.login(username.value, password.value, captchaKey.value, captchaInput.value);
    router.replace("/");
  } catch (e) {
    error.value = e.message;
    refreshCaptcha();
  } finally {
    loading.value = false;
  }
}

onMounted(fetchCaptcha);
</script>

<style scoped>
/* ─── Root ─── */
.login-root {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* ─── Background layers ─── */
.bg-layer {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.bg-charcoal {
  position: absolute;
  inset: 0;
  background: #121010;
}
.bg-glow-top-right {
  position: absolute;
  top: -200px;
  right: -200px;
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(200,60,30,0.2) 0%, rgba(180,50,20,0.08) 30%, transparent 60%);
  filter: blur(80px);
}
.bg-glow-bottom-left {
  position: absolute;
  bottom: -200px;
  left: -200px;
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(255,140,66,0.15) 0%, rgba(200,60,30,0.06) 30%, transparent 60%);
  filter: blur(80px);
}
.bg-glow-center {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 50%, rgba(180,50,20,0.04) 0%, transparent 60%);
}
.bg-food-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.04;
  background-image: 
    radial-gradient(circle at 20% 30%, #ff6b35 0.5px, transparent 0.5px),
    radial-gradient(circle at 70% 20%, #ff8c42 0.7px, transparent 0.7px),
    radial-gradient(circle at 40% 70%, #c0392b 0.4px, transparent 0.4px),
    radial-gradient(circle at 80% 60%, #e67e22 0.6px, transparent 0.6px),
    radial-gradient(circle at 10% 80%, #d35400 0.5px, transparent 0.5px),
    radial-gradient(circle at 55% 45%, #ff4a22 0.3px, transparent 0.3px),
    radial-gradient(circle at 90% 85%, #f39c12 0.5px, transparent 0.5px),
    radial-gradient(circle at 25% 15%, #e74c3c 0.4px, transparent 0.4px),
    radial-gradient(circle at 65% 85%, #ff8c42 0.6px, transparent 0.6px),
    radial-gradient(circle at 45% 55%, #d35400 0.3px, transparent 0.3px);
  background-size: 180px 180px;
  filter: blur(1.5px);
}
.bg-noise {
  position: absolute;
  inset: 0;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 256px 256px;
}

/* ─── Layout ─── */
.login-container {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  width: 100%;
  padding: 24px;
}

/* ─── Card ─── */
.login-card {
  position: relative;
  width: 100%;
  max-width: 440px;
  border-radius: 24px;
}

/* Animated flame border */
.card-border {
  position: absolute;
  inset: -2px;
  border-radius: 26px;
  z-index: 0;
  background: conic-gradient(
    from 0deg,
    rgba(255,74,34,0.6),
    rgba(255,140,66,0.8),
    rgba(255,200,100,0.4),
    rgba(255,140,66,0.8),
    rgba(255,74,34,0.6),
    rgba(180,40,20,0.3),
    rgba(255,74,34,0.6)
  );
  animation: flameSpin 4s linear infinite;
  filter: blur(4px);
  opacity: 0.7;
}
.card-border::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 26px;
  background: conic-gradient(
    from 180deg,
    rgba(255,74,34,0.3),
    rgba(255,140,66,0.5),
    transparent,
    rgba(255,140,66,0.5),
    rgba(255,74,34,0.3)
  );
  animation: flameSpin 6s linear infinite reverse;
}
@keyframes flameSpin {
  to { transform: rotate(360deg); }
}

/* Glow rings */
.login-card::before {
  content: "";
  position: absolute;
  inset: -20px;
  border-radius: 44px;
  background: radial-gradient(ellipse at 50% 50%, rgba(255,74,34,0.06) 0%, transparent 70%);
  z-index: -1;
  filter: blur(20px);
}
.login-card::after {
  content: "";
  position: absolute;
  inset: -8px;
  border-radius: 30px;
  background: radial-gradient(ellipse at 50% 50%, rgba(255,140,66,0.08) 0%, transparent 60%);
  z-index: -1;
  filter: blur(12px);
}

/* Card content */
.card-content {
  position: relative;
  z-index: 1;
  background: rgba(32, 20, 18, 0.75);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-radius: 24px;
  padding: 48px 40px 36px;
  border: 1px solid rgba(255,140,66,0.12);
  box-shadow:
    0 0 60px rgba(255,74,34,0.04),
    0 0 120px rgba(255,74,34,0.02),
    inset 0 0 60px rgba(255,140,66,0.02);
}

/* ─── Logo / Title ─── */
.logo-wrap {
  text-align: center;
  margin-bottom: 36px;
}
.logo-box {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  border-radius: 14px;
  background: linear-gradient(135deg, #ff4a22, #ff8c42);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  box-shadow:
    0 0 20px rgba(255,74,34,0.3),
    0 0 40px rgba(255,74,34,0.1);
}
.logo-flame {
  width: 100%;
  height: 100%;
}
.login-title {
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, #F5EFE4 0%, #FFD700 30%, #FF8C42 70%, #FF4A22 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 4px;
  margin: 0 0 8px;
}
.login-subtitle {
  font-size: 13px;
  color: #C9A77A;
  letter-spacing: 6px;
  margin: 0;
  font-weight: 400;
}

/* ─── Form ─── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.form-error {
  background: rgba(220,38,38,0.1);
  border: 1px solid rgba(220,38,38,0.25);
  color: #fca5a5;
  font-size: 13px;
  padding: 10px 14px;
  border-radius: 12px;
  text-align: center;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.field-label {
  font-size: 13px;
  font-weight: 500;
  color: rgba(201,167,122,0.8);
  letter-spacing: 1px;
}
.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.input-wrap input {
  width: 100%;
  background: rgba(0,0,0,0.45);
  border: 1px solid rgba(255,140,66,0.2);
  border-radius: 12px;
  padding: 12px 16px 12px 40px;
  font-size: 14px;
  color: #F5EFE4;
  outline: none;
  transition: all 0.25s ease;
}
.input-wrap input::placeholder {
  color: rgba(201,167,122,0.35);
}
.input-wrap input:focus {
  border-color: rgba(255,140,66,0.5);
  box-shadow: 0 0 0 1px rgba(255,140,66,0.15), 0 0 20px rgba(255,74,34,0.04);
  background: rgba(0,0,0,0.55);
}
.input-icon {
  position: absolute;
  left: 13px;
  width: 18px;
  height: 18px;
  color: rgba(255,140,66,0.4);
  pointer-events: none;
  z-index: 1;
}
.pw-toggle {
  position: absolute;
  right: 12px;
  width: 20px;
  height: 20px;
  color: rgba(201,167,122,0.4);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
  z-index: 1;
}
.pw-toggle:hover {
  color: rgba(255,140,66,0.7);
}
.pw-toggle svg {
  width: 18px;
  height: 18px;
}
.input-wrap input[type="password"] {
  padding-right: 40px;
}
.input-wrap input[type="text"]:not(.captcha-input input) {
  padding-right: 40px;
}

/* ─── Captcha ─── */
.captcha-row {
  display: flex;
  gap: 10px;
  align-items: stretch;
}
.captcha-input {
  flex: 1;
}
.captcha-input input {
  padding-left: 16px;
  height: 100%;
}
.captcha-canvas {
  width: 130px;
  height: 48px;
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid rgba(255,140,66,0.2);
  flex-shrink: 0;
  transition: border-color 0.25s;
}
.captcha-canvas:hover {
  border-color: rgba(255,140,66,0.4);
}

/* ─── Login button ─── */
.login-btn {
  width: 100%;
  padding: 14px 24px;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 700;
  color: #F5EFE4;
  letter-spacing: 6px;
  cursor: pointer;
  background: linear-gradient(135deg, #ff4a22, #ff8c42);
  box-shadow:
    0 0 24px rgba(255,74,34,0.25),
    0 0 48px rgba(255,74,34,0.08);
  transition: all 0.3s ease;
  margin-top: 4px;
}
.login-btn:hover:not(:disabled) {
  box-shadow:
    0 0 36px rgba(255,74,34,0.4),
    0 0 72px rgba(255,74,34,0.12);
  filter: brightness(1.1);
}
.login-btn:active:not(:disabled) {
  transform: scale(0.98);
}
.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(245,239,228,0.3);
  border-top-color: #F5EFE4;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ─── Default accounts ─── */
.default-accounts {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid rgba(255,140,66,0.08);
  text-align: center;
}
.accounts-label {
  font-size: 11px;
  color: rgba(201,167,122,0.4);
  letter-spacing: 2px;
  margin: 0 0 10px;
  text-transform: uppercase;
}
.accounts-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}
.account-item {
  font-size: 12px;
  color: rgba(201,167,122,0.55);
  letter-spacing: 0.5px;
  white-space: nowrap;
}
.account-divider {
  width: 1px;
  height: 14px;
  background: rgba(201,167,122,0.15);
  align-self: center;
}

/* ─── Register link ─── */
.register-link {
  font-size: 13px;
  color: rgba(201,167,122,0.5);
  margin: 0;
  letter-spacing: 0.5px;
  text-align: center;
}
.register-link a {
  color: rgba(201,167,122,0.7);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.register-link a:hover {
  color: #ff8c42;
}
</style>
