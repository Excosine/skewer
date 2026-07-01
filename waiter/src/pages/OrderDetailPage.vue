<template>
  <div v-if="order" class="min-h-screen bg-neutral-950 pb-24 lg:pb-0">
    <!-- Top bar -->
    <div class="sticky top-0 z-10 bg-neutral-950/80 backdrop-blur-xl border-b border-white/5">
      <div class="flex items-center justify-between px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center gap-3">
          <button @click="router.push('/tables/' + order.table_id)" class="text-neutral-500 hover:text-neutral-300 transition-colors cursor-pointer">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          </button>
          <h1 class="text-lg font-bold text-white">{{ order.order_no }}</h1>
        </div>
        <button v-if="isActive" @click="showMenu = true" class="bg-gradient-to-r from-brand-500 to-brand-600 hover:brightness-110 active:brightness-90 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-all shadow-lg shadow-brand-500/20 cursor-pointer">+ 加菜</button>
      </div>
    </div>

    <div class="max-w-6xl mx-auto lg:flex lg:gap-6 lg:px-4 lg:pt-4">
      <div class="lg:flex-1 lg:min-w-0">
        <div class="px-4 sm:px-6 lg:px-0 pt-3 pb-2 text-sm text-neutral-500 flex gap-4 border-b border-white/5 lg:border-b-0">
          <span>桌号 <span class="text-neutral-200 font-medium">{{ order.table_id }}</span></span>
          <span>加价 ¥{{ Number(order.zone_surcharge).toFixed(2) }}</span>
        </div>

        <div v-if="!isActive" class="px-4 sm:px-6 lg:px-0 pt-4">
          <div class="bg-black/30 border border-white/5 rounded-2xl p-4 text-center">
            <p class="text-neutral-400 text-sm">订单已结账</p>
            <button @click="router.push('/tables/' + order.table_id)" class="text-brand-400 hover:brightness-110 text-sm font-semibold mt-1 transition-colors">返回桌详情</button>
          </div>
        </div>

        <div v-if="isActive && items.length === 0" class="text-center py-16 lg:py-24">
          <p class="text-neutral-500 text-sm mb-6">暂未添加菜品，点击右上角「加菜」</p>
          <button @click="handleCancel" class="inline-flex items-center bg-red-500/80 hover:bg-red-500 active:bg-red-600 text-white font-semibold px-6 py-3 rounded-xl transition-all text-sm cursor-pointer">取消订单</button>
        </div>

        <div class="px-4 sm:px-6 lg:px-0 pt-3 space-y-3">
          <div v-for="item in items" :key="item.item_id" class="bg-black/30 border border-white/5 rounded-2xl p-4 hover:border-white/10 transition-all">
            <div class="flex items-center justify-between mb-3">
              <span class="font-semibold text-white">{{ item.skewer_name }}</span>
              <span class="text-sm text-neutral-500">¥{{ Number(item.unit_price).toFixed(2) }}/支</span>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <button @click="change(item, item.count - 1)" :disabled="!isActive" class="w-8 h-8 rounded-xl bg-white/5 border border-white/10 text-neutral-400 text-lg flex items-center justify-center hover:bg-white/10 active:bg-white/15 disabled:opacity-30 transition-all cursor-pointer">−</button>
                <span class="w-10 text-center font-mono text-lg text-white">{{ scanningId === item.item_id ? '...' : item.count }}</span>
                <button @click="change(item, item.count + 1)" :disabled="!isActive" class="w-8 h-8 rounded-xl bg-white/5 border border-white/10 text-neutral-400 text-lg flex items-center justify-center hover:bg-white/10 active:bg-white/15 disabled:opacity-30 transition-all cursor-pointer">+</button>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-sm text-brand-400 font-mono font-semibold min-w-[60px] text-right">¥{{ Number(item.subtotal).toFixed(2) }}</span>
                <template v-if="isActive">
                  <button @click="scan(item.item_id)" class="text-xs bg-white/5 border border-white/10 hover:bg-white/10 text-neutral-400 px-2.5 py-1.5 rounded-xl transition-all cursor-pointer flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  </button>
                  <button @click="remove(item.item_id)" class="text-xs text-neutral-500 hover:text-red-400 transition-colors">删除</button>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isActive && items.length > 0" class="hidden lg:block w-72 shrink-0">
        <div class="sticky top-20 bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-5 shadow-xl">
          <h3 class="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-4">订单汇总</h3>
          <div class="space-y-2 text-sm mb-5">
            <div class="flex justify-between text-neutral-400"><span>签子总计</span><span class="text-white font-mono font-semibold">{{ totalCount }} 支</span></div>
            <div class="flex justify-between text-neutral-400"><span>菜品小计</span><span class="text-white font-mono font-semibold">¥{{ itemsTotal }}</span></div>
            <div v-if="Number(order.zone_surcharge) > 0" class="flex justify-between text-neutral-400"><span>区域加价</span><span class="text-white font-mono font-semibold">¥{{ Number(order.zone_surcharge).toFixed(2) }}</span></div>
            <div class="border-t border-white/10 pt-3 flex justify-between text-brand-400 font-bold"><span>应付合计</span><span class="font-mono text-lg">¥{{ totalPrice }}</span></div>
          </div>
          <button @click="handleClose" class="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 active:from-emerald-600 active:to-emerald-700 text-white font-semibold py-3 rounded-xl transition-all shadow-lg shadow-emerald-500/20 cursor-pointer">结账</button>
        </div>
      </div>
    </div>

    <div v-if="isActive && items.length > 0" class="fixed bottom-0 left-0 right-0 lg:hidden bg-black/60 backdrop-blur-xl border-t border-white/10 px-5 py-4">
      <div class="flex items-center justify-between mb-3"><span class="text-neutral-400 text-sm">{{ totalCount }}支</span><span class="text-brand-400 font-bold font-mono text-lg">¥{{ totalPrice }}</span></div>
      <button @click="handleClose" class="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-white font-semibold py-3 rounded-xl transition-all shadow-lg shadow-emerald-500/20 cursor-pointer">结账</button>
    </div>

    <input ref="fileInput" type="file" accept="image/*" capture="environment" class="hidden" @change="onFile" />
    <MenuPicker v-if="isActive && showMenu" @select="onAdd" @close="showMenu = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "../api";
import AppHeader from "../components/AppHeader.vue";
import MenuPicker from "../components/MenuPicker.vue";
import { useToast } from "../composables/useToast";

const route = useRoute();
const router = useRouter();
const toast = useToast();
const order = ref(null);
const items = ref([]);
const showMenu = ref(false);
const scanningId = ref(null);
const fileInput = ref(null);

const isActive = computed(() => order.value?.status === 0);
const totalCount = computed(() => items.value.reduce((s, it) => s + it.count, 0));
const itemsTotal = computed(() => items.value.reduce((s, it) => s + Number(it.subtotal), 0).toFixed(2));
const totalPrice = computed(() => (Number(itemsTotal.value) + Number(order.value?.zone_surcharge || 0)).toFixed(2));

onMounted(load);

async function load() {
  try { order.value = await api.getOrder(route.params.id); items.value = order.value.items || []; }
  catch { router.push("/"); }
}

async function onAdd(id) {
  try { await api.addItem(route.params.id, { skewer_type_id: id }); showMenu.value = false; await load(); }
  catch (e) { toast.show(e.message); }
}

async function change(item, n) {
  if (n < 0) return;
  items.value = items.value.map((it) => it.item_id === item.item_id ? { ...it, count: n, subtotal: (n * it.unit_price).toFixed(2) } : it);
  try { await api.updateItem(route.params.id, item.item_id, { count: n }); }
  catch { load(); }
}

async function remove(id) {
  const ok = await toast.ask("删除这个菜品？");
  if (!ok) return;
  items.value = items.value.filter((it) => it.item_id !== id);
  try { await api.deleteItem(route.params.id, id); }
  catch { load(); }
}

function scan(id) { fileInput.value.dataset.itemId = id; fileInput.value.click(); }

async function onFile(e) {
  const f = e.target.files[0];
  if (!f) return;
  const id = Number(fileInput.value.dataset.itemId);
  scanningId.value = id;
  try {
    const r = await api.scanItem(route.params.id, id, f);
    items.value = items.value.map((it) => it.item_id === id ? { ...it, count: r.detected_count, subtotal: (r.detected_count * it.unit_price).toFixed(2) } : it);
  } catch (e) { toast.show("识别失败: " + e.message); }
  finally { scanningId.value = null; e.target.value = ""; }
}

async function handleClose() {
  const ok = await toast.ask(`确认结账？合计 ¥${totalPrice.value}`);
  if (!ok) return;
  try { await api.closeOrder(route.params.id); router.push(`/tables/${order.value.table_id}`); }
  catch (e) { toast.show(e.message); }
}

async function handleCancel() {
  const ok = await toast.ask("确认取消此订单？");
  if (!ok) return;
  try { await api.closeOrder(route.params.id); router.push(`/tables/${order.value.table_id}`); }
  catch (e) { toast.show(e.message); }
}
</script>
