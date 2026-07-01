<template>
  <div class="sticky top-0 z-10 bg-white/80 backdrop-blur border-b border-stone-200">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center gap-3">
      <button v-if="back" @click="$emit('back')" class="text-stone-400 hover:text-stone-600 text-sm transition-colors">← 返回</button>
      <div class="flex-1">
        <h1 class="text-lg font-bold text-stone-800">{{ title }}</h1>
        <p v-if="subtitle" class="text-xs text-stone-400">{{ subtitle }}</p>
      </div>
      <slot name="actions" />
      <button v-if="!back" @click="$emit('logout')" class="text-xs text-stone-400 hover:text-stone-600 transition-colors">退出</button>
    </div>
  </div>
</template>

<script setup>
defineProps({ title: String, subtitle: String, back: Boolean });
defineEmits(["logout", "back"]);
</script>
