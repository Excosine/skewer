<template>
  <div class="min-h-dvh flex items-center justify-center px-5">
    <div class="w-full max-w-sm">
      <h1 class="text-3xl font-bold text-amber-600 text-center mb-1">签子计数</h1>
      <p class="text-stone-400 text-sm text-center mb-10">服务员端</p>

      <form @submit.prevent="submit" class="space-y-4">
        <div v-if="error" class="bg-red-50 border border-red-300 text-red-600 text-sm px-4 py-3 rounded-lg">{{ error }}</div>
        <label class="block text-sm text-stone-500">用户名
          <input v-model="username" type="text" required autofocus class="mt-1 w-full bg-white border border-stone-300 rounded-lg px-4 py-3 text-sm focus:border-amber-500 outline-none transition-colors" />
        </label>
        <label class="block text-sm text-stone-500">密码
          <input v-model="password" type="password" required class="mt-1 w-full bg-white border border-stone-300 rounded-lg px-4 py-3 text-sm focus:border-amber-500 outline-none transition-colors" />
        </label>
        <button type="submit" :disabled="loading" class="w-full bg-amber-500 hover:bg-amber-400 active:bg-amber-600 text-white font-semibold py-3 rounded-lg transition-colors disabled:opacity-50">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const auth = useAuthStore();
const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try { await auth.login(username.value, password.value); router.replace("/"); }
  catch (e) { error.value = e.message; }
  finally { loading.value = false; }
}
</script>
