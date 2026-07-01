<template>
  <div v-if="order" class="min-h-dvh pb-24 lg:pb-0">
    <AppHeader :title="order.order_no" back @back="router.push('/tables/' + order.table_id)">
      <template #actions>
        <button v-if="isActive" @click="showMenu = true" class="bg-amber-500 hover:bg-amber-400 active:bg-amber-600 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors">+ 加菜</button>
      </template>
    </AppHeader>

    <div class="max-w-6xl mx-auto lg:flex lg:gap-6 lg:px-4 lg:pt-4">
      <div class="lg:flex-1 lg:min-w-0">
        <div class="px-4 sm:px-6 lg:px-0 pt-3 pb-2 text-sm text-stone-500 flex gap-4 border-b border-stone-200 lg:border-b-0">
          <span>桌号 <span class="text-stone-700 font-medium">{{ order.table_id }}</span></span>
          <span>加价 ¥{{ Number(order.zone_surcharge).toFixed(2) }}</span>
        </div>

        <div v-if="!isActive" class="px-4 sm:px-6 lg:px-0 pt-4">
          <div class="bg-stone-50 border border-stone-200 rounded-xl p-4 text-center">
            <p class="text-stone-500 text-sm">订单已结账</p>
            <button @click="router.push('/tables/' + order.table_id)" class="text-amber-600 hover:text-amber-500 text-sm font-semibold mt-1 transition-colors">返回桌详情</button>
          </div>
        </div>

        <div v-if="isActive && items.length === 0" class="text-center py-16 lg:py-24">
          <p class="text-stone-400 text-sm mb-6">暂未添加菜品，点击右上角「加菜」</p>
          <button @click="handleCancel" class="inline-flex items-center bg-red-500 hover:bg-red-400 active:bg-red-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors text-sm">取消订单</button>
        </div>

        <div class="px-4 sm:px-6 lg:px-0 pt-3 space-y-3">
          <div v-for="item in items" :key="item.item_id" class="bg-white border border-stone-200 rounded-xl p-4">
            <div class="flex items-center justify-between mb-3">
              <span class="font-semibold text-stone-800">{{ item.skewer_name }}</span>
              <span class="text-sm text-stone-400">¥{{ Number(item.unit_price).toFixed(2) }}/支</span>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <button @click="change(item, item.count - 1)" :disabled="!isActive" class="w-8 h-8 rounded-lg bg-stone-100 border border-stone-200 text-stone-600 text-lg flex items-center justify-center active:bg-stone-200 disabled:opacity-30">−</button>
                <span class="w-10 text-center font-mono text-lg text-stone-800">{{ scanningId === item.item_id ? '...' : item.count }}</span>
                <button @click="change(item, item.count + 1)" :disabled="!isActive" class="w-8 h-8 rounded-lg bg-stone-100 border border-stone-200 text-stone-600 text-lg flex items-center justify-center active:bg-stone-200 disabled:opacity-30">+</button>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-sm text-amber-600 font-mono font-semibold min-w-[60px] text-right">¥{{ Number(item.subtotal).toFixed(2) }}</span>
                <template v-if="isActive">
                  <button @click="scan(item.item_id)" class="text-xs bg-stone-100 border border-stone-200 hover:bg-stone-200 text-stone-600 px-2.5 py-1.5 rounded-lg transition-colors">📷</button>
                  <button @click="remove(item.item_id)" class="text-xs text-stone-400 hover:text-red-500 transition-colors">删除</button>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isActive && items.length > 0" class="hidden lg:block w-72 shrink-0">
        <div class="sticky top-24 bg-white border border-stone-200 rounded-xl p-5">
          <h3 class="text-sm font-semibold text-stone-500 mb-4 uppercase tracking-wide">订单汇总</h3>
          <div class="space-y-2 text-sm mb-5">
            <div class="flex justify-between text-stone-500"><span>签子总计</span><span class="text-stone-800 font-mono font-semibold">{{ totalCount }} 支</span></div>
            <div class="flex justify-between text-stone-500"><span>菜品小计</span><span class="text-stone-800 font-mono font-semibold">¥{{ itemsTotal }}</span></div>
            <div v-if="Number(order.zone_surcharge) > 0" class="flex justify-between text-stone-500"><span>区域加价</span><span class="text-stone-800 font-mono font-semibold">¥{{ Number(order.zone_surcharge).toFixed(2) }}</span></div>
            <div class="border-t border-stone-200 pt-3 flex justify-between text-amber-600 font-bold"><span>应付合计</span><span class="font-mono text-lg">¥{{ totalPrice }}</span></div>
          </div>
          <button @click="handleClose" class="w-full bg-emerald-500 hover:bg-emerald-400 active:bg-emerald-600 text-white font-semibold py-3 rounded-xl transition-colors">结账</button>
        </div>
      </div>
    </div>

    <div v-if="isActive && items.length > 0" class="fixed bottom-0 left-0 right-0 lg:hidden bg-white border-t border-stone-200 px-5 py-4">
      <div class="flex items-center justify-between mb-3"><span class="text-stone-500 text-sm">{{ totalCount }}支</span><span class="text-amber-600 font-bold font-mono text-lg">¥{{ totalPrice }}</span></div>
      <button @click="handleClose" class="w-full bg-emerald-500 hover:bg-emerald-400 active:bg-emerald-600 text-white font-semibold py-3 rounded-xl transition-colors">结账</button>
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
