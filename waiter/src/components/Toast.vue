<template>
  <!-- confirm dialog -->
  <Teleport to="body">
    <div v-if="confirmMsg" class="fixed inset-0 z-50 flex items-center justify-center px-5" @click.self="onConfirm(false)">
      <div class="absolute inset-0 bg-black/40" />
      <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 text-center">
        <p class="text-stone-700 text-sm mb-6">{{ confirmMsg }}</p>
        <div class="flex gap-3">
          <button @click="onConfirm(false)" class="flex-1 bg-stone-100 hover:bg-stone-200 text-stone-600 py-2.5 rounded-lg text-sm font-medium transition-colors">取消</button>
          <button @click="onConfirm(true)" class="flex-1 bg-amber-500 hover:bg-amber-400 text-white py-2.5 rounded-lg text-sm font-semibold transition-colors">确认</button>
        </div>
      </div>
    </div>

    <!-- toast -->
    <div v-if="toastMsg" class="fixed top-20 left-1/2 -translate-x-1/2 z-50 px-4 py-3 bg-stone-800 text-white text-sm rounded-xl shadow-lg transition-all">
      {{ toastMsg }}
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from "vue";

const toastMsg = ref("");
const confirmMsg = ref("");
let confirmResolve = null;

function show(msg) {
  toastMsg.value = msg;
  setTimeout(() => { toastMsg.value = ""; }, 2000);
}

function ask(msg) {
  return new Promise((resolve) => {
    confirmMsg.value = msg;
    confirmResolve = resolve;
  });
}

function onConfirm(val) {
  confirmMsg.value = "";
  if (confirmResolve) { confirmResolve(val); confirmResolve = null; }
}

defineExpose({ show, ask });
</script>
