<template>
  <div class="min-h-dvh pb-20">
    <AppHeader title="桌号详情" back @back="router.push('/')" />

    <div v-if="loading" class="flex items-center justify-center pt-20 text-stone-400">加载中...</div>

    <div v-else-if="table" class="max-w-3xl mx-auto px-4 sm:px-6 pt-5">
      <!-- table info -->
      <div :class="['border rounded-xl p-5 mb-6', cardBg]">
        <div class="flex items-center justify-between mb-3">
          <span class="text-2xl font-bold text-stone-800">{{ table.table_code }}</span>
          <span :class="['text-sm px-3 py-1 rounded-full font-medium', badgeClass]">{{ statusText }}</span>
        </div>
        <div class="flex gap-4 text-sm text-stone-500">
          <span>{{ table.zone_name }}</span>
          <span>{{ table.capacity }}座</span>
          <span v-if="Number(table.zone_surcharge) > 0" class="text-amber-600">+{{ table.zone_surcharge }}元加价</span>
        </div>
      </div>

      <!-- cleaning -->
      <div v-if="table.status === 2" class="text-center mb-6">
        <button @click="handleClean" class="bg-stone-500 hover:bg-stone-400 active:bg-stone-600 text-white px-6 py-3 rounded-xl text-sm font-semibold transition-colors">
          完成打扫
        </button>
      </div>

      <!-- active order -->
      <div v-if="activeOrder" class="mb-6">
        <h3 class="text-sm font-semibold text-stone-500 mb-3 uppercase tracking-wide">进行中</h3>
        <div @click="router.push('/orders/' + activeOrder.id)"
          class="bg-amber-50 border border-amber-200 rounded-xl p-5 cursor-pointer hover:border-amber-400 hover:shadow-sm transition-all">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-stone-500">{{ activeOrder.order_no }}</p>
              <p class="text-lg font-bold text-stone-800 mt-1">
                {{ activeOrder.total_count || 0 }}支
                <span class="text-amber-600 ml-2">¥{{ Number(activeOrder.total_price || 0).toFixed(2) }}</span>
              </p>
            </div>
            <div class="text-stone-400">→</div>
          </div>
        </div>
      </div>

      <!-- paid orders -->
      <div v-if="paidOrders.length > 0" class="mb-6">
        <h3 class="text-sm font-semibold text-stone-500 mb-3 uppercase tracking-wide">已结账（{{ paidOrders.length }}单）</h3>
        <div class="space-y-2">
          <div v-for="o in paidOrders" :key="o.id" class="bg-white border border-stone-200 rounded-xl p-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-stone-500">{{ o.order_no }}</p>
                <p class="text-xs text-stone-400 mt-0.5">{{ o.total_count }}支 · {{ fmtTime(o.paid_at) }}</p>
              </div>
              <span class="text-stone-800 font-mono font-semibold">¥{{ Number(o.total_price || 0).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- idle → 开单 -->
      <div v-if="table.status === 0 && !activeOrder" class="text-center py-16">
        <p class="text-stone-400 text-sm mb-6">暂无订单</p>
        <button @click="handleCreate" class="inline-flex items-center gap-2 bg-amber-500 hover:bg-amber-400 active:bg-amber-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors text-base">
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
