import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "../api";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(JSON.parse(localStorage.getItem("user") || "null"));
  const token = computed(() => localStorage.getItem("token") || "");
  const isLoggedIn = computed(() => !!token.value);

  async function login(username, password) {
    const data = await api.login({ username, password });
    localStorage.setItem("token", data.token);
    localStorage.setItem("user", JSON.stringify(data));
    user.value = data;
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    user.value = null;
  }

  return { user, token, isLoggedIn, login, logout };
});
