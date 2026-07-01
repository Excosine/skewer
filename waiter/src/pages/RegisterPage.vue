<template>
  <div class="min-h-screen bg-neutral-950 flex items-center justify-center p-4 relative overflow-hidden">
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-96 h-96 bg-brand-500/20 rounded-full blur-3xl" />
      <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-brand-600/10 rounded-full blur-3xl" />
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-brand-500/5 rounded-full blur-3xl" />
    </div>

    <div class="relative w-full max-w-sm">
      <div class="bg-black/50 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl shadow-brand-500/10">
        <div class="text-center mb-8">
          <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-600 flex items-center justify-center shadow-lg shadow-brand-500/25">
            <span class="text-xl font-bold text-white">签</span>
          </div>
          <h1 class="text-2xl font-bold text-white">注册新账号</h1>
          <p class="text-neutral-500 text-sm mt-1">服务员端</p>
        </div>

        <form @submit.prevent="submit" class="space-y-5">
          <div v-if="error" class="bg-red-500/10 border border-red-500/30 text-red-400 text-sm px-4 py-3 rounded-xl">{{ error }}</div>
          <div v-if="success" class="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm px-4 py-3 rounded-xl">{{ success }}</div>

          <div>
            <label class="block text-sm text-neutral-400 mb-1.5">用户名</label>
            <input v-model="username" type="text" required autofocus
              class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-neutral-600 focus:border-brand-500/50 focus:ring-1 focus:ring-brand-500/30 outline-none transition-all" />
          </div>

          <div>
            <label class="block text-sm text-neutral-400 mb-1.5">姓名</label>
            <input v-model="realName" type="text" required
              class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-neutral-600 focus:border-brand-500/50 focus:ring-1 focus:ring-brand-500/30 outline-none transition-all" />
          </div>

          <div>
            <label class="block text-sm text-neutral-400 mb-1.5">密码</label>
            <input v-model="password" type="password" required minlength="4"
              class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-neutral-600 focus:border-brand-500/50 focus:ring-1 focus:ring-brand-500/30 outline-none transition-all" />
          </div>

          <div>
            <label class="block text-sm text-neutral-400 mb-1.5">验证码</label>
            <div class="flex gap-2">
              <input v-model="captchaInput" type="text" required maxlength="4"
                class="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-neutral-600 focus:border-brand-500/50 focus:ring-1 focus:ring-brand-500/30 outline-none transition-all uppercase tracking-widest" />
              <canvas ref="captchaCanvas" @click="generateCaptcha"
                class="rounded-xl cursor-pointer border border-white/10 w-[120px] h-[46px] shrink-0" />
            </div>
            <p class="text-xs text-neutral-600 mt-1">点击图片刷新验证码</p>
          </div>

          <button type="submit" :disabled="loading"
            class="w-full bg-gradient-to-r from-brand-500 to-brand-600 hover:brightness-110 active:brightness-90 text-white font-semibold py-3 rounded-xl transition-all disabled:opacity-50 shadow-lg shadow-brand-500/25">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>

        <p class="text-center text-sm text-neutral-500 mt-6">
          已有账号？
          <router-link to="/login" class="text-brand-400 hover:brightness-110 transition-colors">去登录</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { api } from "../api";

const router = useRouter();
const username = ref("");
const realName = ref("");
const password = ref("");
const captchaInput = ref("");
const captchaAnswer = ref("");
const captchaCanvas = ref(null);
const error = ref("");
const success = ref("");
const loading = ref(false);

const CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";

function generateCaptcha() {
  const canvas = captchaCanvas.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  canvas.width = 120;
  canvas.height = 46;
  ctx.fillStyle = "#f5f5f0";
  ctx.fillRect(0, 0, 120, 46);
  let code = "";
  for (let i = 0; i < 4; i++) code += CHARS[Math.floor(Math.random() * CHARS.length)];
  captchaAnswer.value = code;
  for (let i = 0; i < 6; i++) {
    ctx.strokeStyle = `rgba(180,150,100,${0.1 + Math.random() * 0.2})`;
    ctx.lineWidth = 1 + Math.random() * 2;
    ctx.beginPath();
    ctx.moveTo(Math.random() * 120, Math.random() * 46);
    ctx.lineTo(Math.random() * 120, Math.random() * 46);
    ctx.stroke();
  }
  ctx.font = "bold 24px 'Courier New', monospace";
  ctx.textBaseline = "middle";
  const x0 = 10;
  code.split("").forEach((ch, i) => {
    const rot = (Math.random() - 0.5) * 0.4;
    const y = 24 + (Math.random() - 0.5) * 8;
    ctx.save();
    ctx.translate(x0 + i * 26, y);
    ctx.rotate(rot);
    ctx.fillStyle = ["#a16207", "#b45309", "#d97706", "#92400e"][i % 4];
    ctx.fillText(ch, 0, 0);
    ctx.restore();
  });
  for (let i = 0; i < 30; i++) {
    ctx.fillStyle = `rgba(120,80,40,${Math.random() * 0.3})`;
    ctx.beginPath();
    ctx.arc(Math.random() * 120, Math.random() * 46, 1 + Math.random() * 2, 0, Math.PI * 2);
    ctx.fill();
  }
}

async function submit() {
  error.value = "";
  success.value = "";
  if (captchaInput.value.toUpperCase() !== captchaAnswer.value) {
    error.value = "验证码错误";
    generateCaptcha();
    captchaInput.value = "";
    return;
  }
  loading.value = true;
  try {
    await api.register({ username: username.value, password: password.value, real_name: realName.value });
    success.value = "注册成功，正在跳转登录...";
    setTimeout(() => router.replace("/login"), 1500);
  } catch (e) {
    error.value = e.message;
    generateCaptcha();
    captchaInput.value = "";
  } finally {
    loading.value = false;
  }
}

onMounted(generateCaptcha);
</script>
