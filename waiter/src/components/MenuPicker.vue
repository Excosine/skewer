<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-end sm:items-center justify-center" @click.self="$emit('close')">
      <div class="absolute inset-0 bg-black/30" />
      <div class="relative bg-white border border-stone-200 rounded-t-2xl sm:rounded-2xl shadow-xl w-full max-w-lg max-h-[70dvh] flex flex-col overflow-hidden">
        <div class="flex items-center justify-between px-5 py-4 border-b border-stone-200 shrink-0">
          <h2 class="text-base font-semibold text-stone-800">选择菜品</h2>
          <button @click="$emit('close')" class="text-stone-400 hover:text-stone-600 text-lg leading-none">✕</button>
        </div>
        <div class="flex gap-1 px-5 py-3 border-b border-stone-100 overflow-x-auto shrink-0">
          <button v-for="c in categories" :key="c.id" @click="active = c.id" :class="['text-sm px-3 py-1.5 rounded-lg whitespace-nowrap transition-colors', active === c.id ? 'bg-amber-100 text-amber-700' : 'text-stone-400 hover:text-stone-600']">{{ c.name }}</button>
        </div>
        <div class="flex-1 overflow-y-auto px-5 py-3 space-y-1">
          <div v-if="loading" class="text-center text-stone-400 py-8">加载中...</div>
          <button v-for="s in filtered" :key="s.id" @click="$emit('select', s.id)" class="w-full flex items-center justify-between px-3 py-3 rounded-lg hover:bg-stone-50 active:bg-stone-100 transition-colors text-left">
            <span class="text-sm text-stone-700">{{ s.skewer_name }}</span>
            <span class="text-sm text-amber-600 font-mono font-medium">¥{{ s.unit_price }}/支</span>
          </button>
          <p v-if="!loading && filtered.length === 0" class="text-stone-400 text-sm text-center py-8">暂无菜品</p>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { api } from "../api";

defineEmits(["select", "close"]);
const categories = ref([]);
const skewers = ref([]);
const active = ref(null);
const loading = ref(true);

onMounted(async () => {
  const [cats, skews] = await Promise.all([api.categories(), api.skewers()]);
  categories.value = cats;
  skewers.value = skews;
  if (cats.length) active.value = cats[0].id;
  loading.value = false;
});

const filtered = computed(() => {
  const cat = categories.value.find((c) => c.id === active.value);
  return skewers.value.filter((s) => cat && s.category_name === cat.name);
});
</script>
