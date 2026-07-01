<script setup>
const props = defineProps({
  label: String,
  value: [Number, String],
  unit: String
})
</script>

<template>
  <div class="stat-card">
    <!-- 数值区域 -->
    <div class="stat-value">
      <span class="number">{{ value }}</span>
      <span v-if="unit" class="unit">{{ unit }}</span>
    </div>
    <!-- 标签区域 -->
    <div class="stat-label">{{ label }}</div>
    <!-- 暖色光晕装饰 -->
    <div class="card-glow"></div>
  </div>
</template>

<style scoped lang="scss">
.stat-card {
  min-width: 200px;
  flex: 1;
  max-width: 280px;
  height: 100px;
  background: rgba(26, 21, 18, 0.6);
  border: 1px solid rgba(248, 245, 242, 0.08);
  border-radius: 16px;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  transition: all 250ms ease;
  box-shadow: 0 8px 32px rgba(15, 12, 10, 0.3);

  // 卡片顶部暖色点缀
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 16px;
    right: 16px;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(217, 72, 54, 0.15), transparent);
  }

  &:hover {
    border-color: rgba(242, 112, 68, 0.15);
    box-shadow: 0 12px 40px rgba(242, 112, 68, 0.1);
    transform: translateY(-3px);
  }

  // 暖色光晕装饰
  .card-glow {
    position: absolute;
    bottom: -20px;
    right: -20px;
    width: 80px;
    height: 80px;
    background: radial-gradient(circle, rgba(217, 72, 54, 0.08) 0%, transparent 70%);
    pointer-events: none;
  }

  .stat-value {
    display: flex;
    align-items: baseline;
    gap: 6px;

    .number {
      font-size: 28px;
      font-weight: 700;
      font-family: 'SF Mono', 'Consolas', monospace;
      color: #F8F5F2;
      letter-spacing: 1px;
      background: linear-gradient(to right, #D94836, #E6B87D);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .unit {
      font-size: 14px;
      font-weight: 500;
      color: #BFAFA6;
    }
  }

  .stat-label {
    font-size: 14px;
    font-weight: 500;
    color: #BFAFA6;
    letter-spacing: 1px;
  }
}
</style>