<template>
  <div class="min-h-screen bg-neutral-950">
    <!-- Top bar -->
    <div class="sticky top-0 z-10 bg-neutral-950/80 backdrop-blur-xl border-b border-white/5">
      <div class="flex items-center gap-3 px-4 sm:px-6 lg:px-8 py-4">
        <button @click="router.push('/')" class="text-neutral-500 hover:text-neutral-300 transition-colors text-sm cursor-pointer">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </button>
        <h1 class="text-lg font-bold text-white">桌号详情</h1>
      </div>
    </div>

    <div v-if="loading" class="flex items-center justify-center pt-20 text-neutral-500">加载中...</div>

    <div v-else-if="table" class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-20 space-y-6">
      <!-- table info -->
      <div class="rounded-2xl p-6 border detail-card" :class="cardBg">
        <div class="flex items-center justify-between mb-3">
          <span class="text-2xl font-bold text-white">{{ table.table_code }}</span>
          <span :class="['text-xs px-3 py-1 rounded-full font-medium', badgeClass]">{{ statusText }}</span>
        </div>
        <div class="flex gap-4 text-sm text-neutral-400">
          <span>{{ table.zone_name }}</span>
          <span>{{ table.capacity }}座</span>
          <span v-if="Number(table.zone_surcharge) > 0" class="text-brand-400">+{{ table.zone_surcharge }}元加价</span>
        </div>
      </div>

      <!-- cleaning -->
      <div v-if="table.status === 2" class="text-center">
        <button @click="handleClean" class="bg-neutral-700 hover:bg-neutral-600 active:bg-neutral-800 text-white px-6 py-3 rounded-xl text-sm font-semibold transition-all cursor-pointer">
          完成打扫
        </button>
      </div>

      <!-- active order -->
      <div v-if="activeOrder">
        <h3 class="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-3">进行中</h3>
        <div @click="router.push('/orders/' + activeOrder.id)"
          class="bg-brand-500/10 border border-brand-500/20 rounded-2xl p-5 cursor-pointer hover:border-brand-500/40 hover:shadow-lg hover:shadow-brand-500/5 transition-all">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-neutral-400">{{ activeOrder.order_no }}</p>
              <p class="text-lg font-bold text-white mt-1">
                {{ activeOrder.total_count || 0 }}支
                <span class="text-brand-400 ml-2">¥{{ Number(activeOrder.total_price || 0).toFixed(2) }}</span>
              </p>
            </div>
            <svg class="w-5 h-5 text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </div>
        </div>
      </div>

      <!-- paid orders -->
      <div v-if="paidOrders.length > 0">
        <h3 class="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-3">已结账（{{ paidOrders.length }}单）</h3>
        <div class="space-y-2">
          <div v-for="o in paidOrders" :key="o.id" class="bg-black/30 border border-white/5 rounded-2xl p-4 transition-all hover:border-white/10">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-neutral-300">{{ o.order_no }}</p>
                <p class="text-xs text-neutral-500 mt-0.5">{{ o.total_count }}支 · {{ fmtTime(o.paid_at) }}</p>
              </div>
              <span class="text-white font-mono font-semibold">¥{{ Number(o.total_price || 0).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- idle → 开单 -->
      <div v-if="table.status === 0 && !activeOrder" class="text-center py-16">
        <p class="text-neutral-500 text-sm mb-6">暂无订单</p>
        <button @click="handleCreate" class="inline-flex items-center gap-2 bg-gradient-to-r from-brand-500 to-brand-600 hover:brightness-110 active:brightness-90 text-white font-semibold px-6 py-3 rounded-xl transition-all text-base shadow-lg shadow-brand-500/25 cursor-pointer">
          开单
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "../api";
import { useToast } from "../composables/useToast";
import AppHeader from "../components/AppHeader.vue";

const route = useRoute();
const router = useRouter();
const toast = useToast();
const table = ref(null);
const loading = ref(true);

onMounted(load);

async function load() {
  try {
    const data = await api.tableDetail(route.params.id);
    table.value = data;
  } catch { router.push("/"); }
  loading.value = false;
}

const activeOrder = computed(() => {
  if (!table.value) return null;
  return table.value.orders.find((o) => o.status === 0) || null;
});
const paidOrders = computed(() => {
  if (!table.value) return [];
  return table.value.orders.filter((o) => o.status === 1);
});
const statusText = computed(() => ({ 0: "空闲", 1: "占用", 2: "清洁" }[table.value?.status]));
const cardBg = computed(() => ({ 0: "bg-white border-stone-200", 1: "bg-amber-50 border-amber-200", 2: "bg-stone-50 border-stone-200" }[table.value?.status]));
const badgeClass = computed(() => ({ 0: "bg-stone-100 text-stone-500", 1: "bg-amber-100 text-amber-700", 2: "bg-stone-200 text-stone-500" }[table.value?.status]));

async function handleCreate() {
  try {
    const order = await api.createOrder({ table_id: table.value.id });
    router.push(`/orders/${order.id}`);
  } catch (e) { toast.show(e.message); }
}

async function handleClean() {
  const ok = await toast.ask("确认打扫完成？");
  if (!ok) return;
  try {
    await api.updateTable(table.value.id, { status: 0 });
    await load();
  } catch (e) { toast.show(e.message); }
}

function fmtTime(ts) {
  if (!ts) return "";
  const d = new Date(ts);
  return `${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`;
}
</script>

<style>
.detail-card {
  background: rgba(42, 31, 26, 0.7) !important;
  border-color: rgba(255, 255, 255, 0.05) !important;
}
</style>
