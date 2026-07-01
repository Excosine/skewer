<template>
  <div class="min-h-dvh pb-20">
    <AppHeader title="桌况" :subtitle="auth.user?.real_name" @logout="auth.logout" />

    <div v-if="loading" class="flex items-center justify-center pt-20 text-stone-400">加载中...</div>

    <div v-else class="max-w-6xl mx-auto px-4 sm:px-6 pt-5">
      <div v-for="zone in zones" :key="zone" class="mb-8">
        <div class="flex items-center gap-2 mb-3">
          <h2 class="text-sm font-semibold text-stone-600">{{ zone }}</h2>
          <span v-if="zoneSurcharge(zone) > 0" class="text-xs text-amber-600 bg-amber-50 px-2 py-0.5 rounded">+{{ zoneSurcharge(zone) }}元</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
          <button v-for="t in zoneTables(zone)" :key="t.table_id" @click="router.push('/tables/' + t.table_id)"
            :class="['border rounded-xl p-4 text-left transition-all active:scale-[0.98]', cardClass(t)]">
            <div class="flex items-center justify-between mb-2">
              <span class="text-lg font-bold">{{ t.table_code }}</span>
              <span :class="['text-xs px-2 py-0.5 rounded-full font-medium', badgeClass(t)]">{{ statusText(t.table_status) }}</span>
            </div>
            <p class="text-xs text-stone-400">
              {{ t.capacity }}座
              <template v-if="t.total_price > 0"> · ¥{{ Number(t.total_price).toFixed(0) }}</template>
            </p>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { api } from "../api";
import AppHeader from "../components/AppHeader.vue";

const router = useRouter();
const auth = useAuthStore();
const tables = ref([]);
const loading = ref(true);

onMounted(async () => {
  try { tables.value = await api.tables(); }
  catch { router.push("/login"); }
  loading.value = false;
});

const zones = computed(() => [...new Set(tables.value.map((t) => t.zone_name))]);
function zoneTables(z) { return tables.value.filter((t) => t.zone_name === z); }
function zoneSurcharge(z) { const t = tables.value.find((t) => t.zone_name === z); return t ? Number(t.zone_surcharge) : 0; }
function statusText(s) { return { 0: "空闲", 1: "占用", 2: "清洁" }[s]; }
function cardClass(t) {
  return { 0: "bg-white border-stone-200 hover:border-amber-300 hover:shadow-sm", 1: "bg-amber-50 border-amber-200 hover:border-amber-400", 2: "bg-stone-50 border-stone-200 hover:border-stone-400" }[t.table_status];
}
function badgeClass(t) {
  return { 0: "bg-stone-100 text-stone-500", 1: "bg-amber-100 text-amber-700", 2: "bg-stone-200 text-stone-500" }[t.table_status];
}
</script>
