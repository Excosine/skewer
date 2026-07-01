<template>
  <Toast ref="toast" />
  <router-view />
</template>

<script setup>
import { ref, provide, onMounted } from "vue";
import Toast from "./components/Toast.vue";

const toast = ref(null);

provide("$toast", {
  show: (msg) => toast.value?.show(msg),
  ask: (msg) => toast.value?.ask(msg),
});
</script>
