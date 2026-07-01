<template>
  <div class="min-h-screen" style="background: #121010">
    <div class="fixed inset-0 pointer-events-none" style="background: radial-gradient(ellipse at 30% 20%, rgba(180,60,30,0.07) 0%, transparent 60%), radial-gradient(ellipse at 70% 80%, rgba(200,50,20,0.04) 0%, transparent 50%)" />
    <div class="relative flex min-h-screen">
      <!-- Sidebar -->
      <aside class="hidden lg:flex flex-col w-60 shrink-0" style="background: rgba(42, 26, 22, 0.55); backdrop-filter: blur(24px); border-right: 1px solid rgba(255,255,255,0.04);">
        <div class="flex items-center gap-3 px-6 py-5" style="border-bottom: 1px solid rgba(255,255,255,0.04);">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-[#ff4a22] to-[#ff8c42] flex items-center justify-center shadow-lg" style="box-shadow: 0 0 16px rgba(255,74,34,0.25);">
            <span class="text-sm font-bold text-[#F5EFE4]">签</span>
          </div>
          <div>
            <h1 class="text-sm font-bold text-[#F5EFE4]">签子计数</h1>
            <p class="text-[10px] text-[#C9A77A]">服务员端</p>
          </div>
        </div>
        <nav class="flex-1 px-3 py-4 space-y-1">
          <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#F5EFE4] font-medium"
            style="background: rgba(255,74,34,0.12); border-left: 3px solid #ff4a22; border-radius: 0 8px 8px 0; margin-left: -12px; padding-left: 15px;">
            <svg class="w-4 h-4 text-[#ff8c42]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
            桌台管理
          </a>
        </nav>
        <div class="px-3 py-4" style="border-top: 1px solid rgba(255,255,255,0.04);">
          <button @click="auth.logout" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#C9A77A] hover:text-[#F5EFE4] transition-all w-full cursor-pointer hover:bg-white/5">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
            退出登录
          </button>
        </div>
      </aside>

      <!-- Main -->
      <div class="flex-1 flex flex-col min-w-0">
        <!-- Top bar -->
        <div class="sticky top-0 z-10" style="background: rgba(18,16,16,0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.04);">
          <div class="flex items-center justify-between px-6 lg:px-8 py-4">
            <div>
              <h1 class="text-lg font-bold text-[#F5EFE4]">桌况</h1>
              <p v-if="auth.user?.real_name" class="text-xs text-[#C9A77A]">{{ auth.user?.real_name }}</p>
            </div>
            <div class="flex items-center gap-3">
              <button @click="auth.logout" class="text-xs text-[#C9A77A] hover:text-[#F5EFE4] transition-colors cursor-pointer">退出</button>
            </div>
          </div>
        </div>

        <div v-if="loading" class="flex-1 flex items-center justify-center text-[#C9A77A]">加载中...</div>

        <div v-else class="flex-1 overflow-y-auto px-6 lg:px-8 py-6 space-y-6">
          <!-- Stats cards -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="rounded-2xl p-5" :style="statCardStyle">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-medium uppercase tracking-wider" style="color: rgba(201,167,122,0.6);">总桌台</span>
                <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: rgba(255,74,34,0.12);">
                  <svg class="w-4 h-4 text-[#ff8c42]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                </div>
              </div>
              <p class="text-2xl font-bold text-[#F5EFE4]">{{ tables.length }}</p>
            </div>
            <div class="rounded-2xl p-5" :style="statCardStyle">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-medium uppercase tracking-wider" style="color: rgba(201,167,122,0.6);">占用</span>
                <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: rgba(255,74,34,0.12);">
                  <svg class="w-4 h-4 text-[#ff8c42]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
              </div>
              <p class="text-2xl font-bold text-[#ff8c42]">{{ tables.filter(t => t.table_status === 1).length }}</p>
            </div>
            <div class="rounded-2xl p-5" :style="statCardStyle">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-medium uppercase tracking-wider" style="color: rgba(201,167,122,0.6);">空闲</span>
                <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: rgba(52,211,153,0.1);">
                  <svg class="w-4 h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                </div>
              </div>
              <p class="text-2xl font-bold text-emerald-400">{{ tables.filter(t => t.table_status === 0).length }}</p>
            </div>
            <div class="rounded-2xl p-5" :style="statCardStyle">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-medium uppercase tracking-wider" style="color: rgba(201,167,122,0.6);">清洁中</span>
                <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: rgba(255,255,255,0.04);">
                  <svg class="w-4 h-4" style="color: rgba(255,255,255,0.3);" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                </div>
              </div>
              <p class="text-2xl font-bold" style="color: rgba(255,255,255,0.5);">{{ tables.filter(t => t.table_status === 2).length }}</p>
            </div>
          </div>

          <!-- Chart + zones -->
          <div class="lg:flex lg:gap-6 space-y-6 lg:space-y-0">
            <!-- Status summary -->
            <div class="lg:w-72 shrink-0">
              <div class="rounded-2xl p-5 h-full flex flex-col justify-between" :style="panelStyle">
                <div>
                  <h3 class="text-xs font-medium text-[#C9A77A] uppercase tracking-wider mb-4">桌台状态分布</h3>
                  <div class="space-y-4">
                    <div v-for="d in distribution" :key="d.label">
                      <div class="flex items-center justify-between text-xs mb-1.5">
                        <span class="flex items-center gap-1.5" :style="{ color: d.labelColor }">
                          <span class="w-2 h-2 rounded-full" :style="{ background: d.dotColor }" />{{ d.label }}
                        </span>
                        <span class="font-semibold text-[#F5EFE4]">{{ d.count }}</span>
                      </div>
                      <div class="h-1.5 rounded-full overflow-hidden" style="background: rgba(255,255,255,0.06);">
                        <div class="h-full rounded-full transition-all" :style="{ width: d.pct + '%', background: d.barGradient }" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Zone grids -->
            <div class="flex-1 min-w-0 space-y-6">
              <div v-for="zone in zones" :key="zone">
                <div class="flex items-center gap-2 mb-3">
                  <h2 class="text-sm font-semibold text-[#F5EFE4]">{{ zone }}</h2>
                  <span v-if="zoneSurcharge(zone) > 0" class="text-[10px] font-medium px-2 py-0.5 rounded-full" style="background: linear-gradient(135deg, rgba(255,74,34,0.15), rgba(255,140,66,0.1)); color: #ff8c42; border: 1px solid rgba(255,74,34,0.2);">+{{ zoneSurcharge(zone) }}元</span>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
                  <button v-for="t in zoneTables(zone)" :key="t.table_id" @click="router.push('/tables/' + t.table_id)"
                    class="rounded-2xl px-5 py-5 text-left transition-all active:scale-[0.97] cursor-pointer"
                    :class="'tc-' + t.table_status">
                    <div class="flex items-start justify-between mb-3">
                      <span class="text-[28px] font-bold leading-none tracking-tight text-[#F5EFE4] font-mono">{{ t.table_code }}</span>
                      <span class="mt-0.5 flex items-center gap-1.5 text-[11px] font-medium" :style="{ color: statusTextColor(t.table_status) }">
                        <span class="w-1.5 h-1.5 rounded-full" :style="{ background: statusDotColor(t.table_status) }" />
                        {{ statusText(t.table_status) }}
                      </span>
                    </div>
                    <div class="flex items-center gap-2 text-xs text-[#C9A77A]">
                      <span>{{ t.capacity }}人桌</span>
                      <span style="color: rgba(201,167,122,0.3);">|</span>
                      <span>{{ zone }}</span>
                      <template v-if="t.total_price > 0">
                        <span style="color: rgba(201,167,122,0.3);">·</span>
                        <span class="font-semibold text-[#ff8c42]">¥{{ Number(t.total_price).toFixed(0) }}</span>
                      </template>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
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
function statusDotColor(s) { return { 0: "#34d399", 1: "#ff4a22", 2: "rgba(255,255,255,0.25)" }[s]; }
function statusTextColor(s) { return { 0: "#34d399", 1: "#ff8c42", 2: "rgba(255,255,255,0.3)" }[s]; }

const statCardStyle = {
  background: "rgba(42, 26, 22, 0.5)",
  backdropFilter: "blur(12px)",
  border: "1px solid rgba(255,74,34,0.22)",
  boxShadow: "0 0 20px rgba(255,74,34,0.04)",
};
const panelStyle = {
  background: "rgba(42, 26, 22, 0.45)",
  backdropFilter: "blur(12px)",
  border: "1px solid rgba(255,255,255,0.04)",
  borderRadius: "16px",
};

const distribution = computed(() => {
  const total = tables.value.length || 1;
  const occupied = tables.value.filter((t) => t.table_status === 1).length;
  const free = tables.value.filter((t) => t.table_status === 0).length;
  const cleaning = tables.value.filter((t) => t.table_status === 2).length;
  return [
    { label: "空闲", count: free, dotColor: "#34d399", labelColor: "rgba(201,167,122,0.7)", barGradient: "linear-gradient(90deg, #34d399, #6ee7b7)", pct: (free / total) * 100 },
    { label: "占用", count: occupied, dotColor: "#ff4a22", labelColor: "rgba(201,167,122,0.7)", barGradient: "linear-gradient(90deg, #ff4a22, #ff8c42)", pct: (occupied / total) * 100 },
    { label: "清洁", count: cleaning, dotColor: "rgba(255,255,255,0.2)", labelColor: "rgba(201,167,122,0.7)", barGradient: "linear-gradient(90deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05))", pct: (cleaning / total) * 100 },
  ];
});
</script>

<style>
/* Table card base */
button[class*="tc-"] {
  background: rgba(42, 26, 22, 0.6);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.2s ease;
}
button[class*="tc-"]:hover {
  box-shadow: 0 0 24px rgba(255, 74, 34, 0.08);
}
button[class*="tc-"]:active {
  transform: scale(0.97);
}

/* 空闲 - light green glow border */
.tc-0 {
  border-color: rgba(52, 211, 153, 0.15);
}
.tc-0:hover {
  border-color: rgba(52, 211, 153, 0.35);
  box-shadow: 0 0 20px rgba(52, 211, 153, 0.06);
}

/* 占用 - thick orange-red flame glow border */
.tc-1 {
  border-color: rgba(255, 74, 34, 0.35);
  border-width: 1.5px;
  box-shadow: 0 0 16px rgba(255, 74, 34, 0.04), inset 0 0 20px rgba(255, 74, 34, 0.02);
}
.tc-1:hover {
  border-color: rgba(255, 74, 34, 0.6);
  box-shadow: 0 0 28px rgba(255, 74, 34, 0.1), inset 0 0 24px rgba(255, 74, 34, 0.04);
}

/* 清洁 - matte gray thin border */
.tc-2 {
  border-color: rgba(255, 255, 255, 0.04);
}
.tc-2:hover {
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 16px rgba(255, 255, 255, 0.02);
}
</style>
