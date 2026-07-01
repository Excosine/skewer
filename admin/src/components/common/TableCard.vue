<script setup>
const props = defineProps({
  tableCode: String,
  status: Number,
  totalCount: Number,
  totalPrice: Number
})

const emit = defineEmits(['click'])

const statusMap = {
  0: { class: 'idle', text: '空闲' },
  1: { class: 'occupied', text: '占用' },
  2: { class: 'cleaning', text: '清洁中' }
}

const currentStatus = statusMap[props.status] || statusMap[0]

const handleClick = () => {
  emit('click', {
    tableCode: props.tableCode,
    status: props.status
  })
}
</script>

<template>
  <div
    class="table-card"
    :class="currentStatus.class"
    @click="handleClick"
  >
    <!-- 桌号 - 鎏金效果 -->
    <div class="table-code">{{ tableCode }}</div>

    <!-- 空闲状态 -->
    <div v-if="status === 0" class="status-text">
      空闲可用
    </div>

    <!-- 占用状态 - 鎏金数据显示 -->
    <div v-if="status === 1" class="occupied-info">
      <div class="table-count">{{ totalCount }}签</div>
      <div class="table-price">¥{{ totalPrice }}</div>
      <div class="status-badge">占用中</div>
    </div>

    <!-- 清洁中状态 -->
    <div v-if="status === 2" class="cleaning-info">
      <div class="status-text">清洁整理</div>
      <div class="cleaning-progress">
        <div class="progress-bar"></div>
      </div>
    </div>

    <!-- 状态指示灯 -->
    <div class="status-indicator" :class="currentStatus.class"></div>
  </div>
</template>

<style scoped lang="scss">
.table-card {
  // 放大卡片尺寸到 120px
  width: 120px;
  height: 120px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 300ms ease;
  position: relative;
  overflow: hidden;
  // 统一内边距
  padding: 16px 12px;
  box-sizing: border-box;

  // 空闲状态 - 暖灰调 + 立体阴影
  &.idle {
    background: rgba(107, 91, 83, 0.2);
    border: 2px solid rgba(107, 91, 83, 0.35);
    color: #BFAFA6;
    box-shadow:
      0 4px 12px rgba(15, 12, 10, 0.15),
      inset 0 1px 0 rgba(248, 245, 242, 0.03);

    &:hover {
      background: rgba(107, 91, 83, 0.3);
      border-color: rgba(107, 91, 83, 0.5);
      transform: translateY(-6px) scale(1.02);
      box-shadow:
        0 8px 24px rgba(15, 12, 10, 0.25),
        0 0 16px rgba(107, 91, 83, 0.1);
    }

    .status-indicator.idle {
      background: #BFAFA6;
      box-shadow: 0 0 8px rgba(191, 175, 166, 0.3);
    }
  }

  // 占用状态 - 牛油红 + 鎏金 + 立体发光
  &.occupied {
    background: linear-gradient(135deg, rgba(217, 72, 54, 0.3), rgba(242, 112, 68, 0.2));
    border: 2px solid rgba(217, 72, 54, 0.5);
    color: #F8F5F2;
    box-shadow:
      0 4px 20px rgba(217, 72, 54, 0.25),
      0 0 24px rgba(217, 72, 54, 0.15),
      inset 0 1px 0 rgba(248, 245, 242, 0.05);

    &:hover {
      transform: translateY(-6px) scale(1.02);
      box-shadow:
        0 8px 32px rgba(217, 72, 54, 0.35),
        0 0 32px rgba(217, 72, 54, 0.25),
        inset 0 1px 0 rgba(248, 245, 242, 0.08);
      border-color: rgba(217, 72, 54, 0.7);
    }

    // 内部光晕
    &::before {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at center, rgba(230, 184, 125, 0.08) 0%, transparent 70%);
      pointer-events: none;
    }

    .status-indicator.occupied {
      background: #D94836;
      box-shadow: 0 0 12px rgba(217, 72, 54, 0.5);
      animation: glow-occupied 2s ease-in-out infinite;
    }
  }

  // 清洁中状态 - 烟火橙 + 立体效果
  &.cleaning {
    background: linear-gradient(135deg, rgba(242, 112, 68, 0.25), rgba(230, 184, 125, 0.15));
    border: 2px solid rgba(242, 112, 68, 0.4);
    color: #F8F5F2;
    box-shadow:
      0 4px 16px rgba(242, 112, 68, 0.2),
      0 0 20px rgba(242, 112, 68, 0.1),
      inset 0 1px 0 rgba(248, 245, 242, 0.04);

    &:hover {
      transform: translateY(-6px) scale(1.02);
      box-shadow:
        0 8px 24px rgba(242, 112, 68, 0.3),
        0 0 28px rgba(242, 112, 68, 0.2);
      border-color: rgba(242, 112, 68, 0.6);
    }

    // 内部光晕
    &::before {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at center, rgba(230, 184, 125, 0.05) 0%, transparent 70%);
      pointer-events: none;
    }

    .status-indicator.cleaning {
      background: #F27044;
      box-shadow: 0 0 12px rgba(242, 112, 68, 0.4);
      animation: glow-cleaning 2s ease-in-out infinite;
    }
  }
}

// 桌号 - 鎏金渐变效果
.table-code {
  font-size: 24px;
  font-weight: 700;
  font-family: 'SF Mono', 'Consolas', monospace;
  letter-spacing: 2px;
  color: #E6B87D;
  text-shadow:
    0 0 12px rgba(230, 184, 125, 0.4),
    0 2px 4px rgba(15, 12, 10, 0.3);
  // 鎏金渐变文字
  background: linear-gradient(135deg, #E6B87D 0%, #F27044 50%, #D94836 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  // 固定高度和行高，确保对齐
  height: 28px;
  line-height: 28px;
  flex-shrink: 0;
}

.status-text {
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 2px;
  color: #BFAFA6;
  text-shadow: 0 0 4px rgba(191, 175, 166, 0.2);
  // 固定高度和行高，确保对齐
  height: 20px;
  line-height: 20px;
  flex-shrink: 0;
  margin-top: 8px;
}

// 占用状态信息 - 鎏金风格，固定行间距
.occupied-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  // 固定行间距
  gap: 6px;
  margin-top: 8px;

  .table-count {
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 1px;
    color: #F8F5F2;
    // 固定高度确保对齐
    height: 20px;
    line-height: 20px;
    flex-shrink: 0;
  }

  .table-price {
    font-size: 20px;
    font-weight: 700;
    color: #E6B87D;
    text-shadow: 0 0 10px rgba(230, 184, 125, 0.5);
    background: linear-gradient(135deg, #E6B87D, #F27044);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    // 固定高度确保对齐
    height: 24px;
    line-height: 24px;
    flex-shrink: 0;
  }

  .status-badge {
    font-size: 11px;
    padding: 3px 10px;
    background: rgba(217, 72, 54, 0.3);
    border: 1px solid rgba(217, 72, 54, 0.4);
    border-radius: 4px;
    color: #F8F5F2;
    letter-spacing: 1px;
    // 固定高度确保对齐
    height: 18px;
    line-height: 12px;
    flex-shrink: 0;
  }
}

// 清洁中信息 - 固定行间距
.cleaning-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  // 固定行间距
  gap: 8px;
  margin-top: 8px;

  .status-text {
    color: #F27044;
    font-weight: 600;
    height: 20px;
    line-height: 20px;
  }

  .cleaning-progress {
    width: 80px;
    height: 4px;
    background: rgba(242, 112, 68, 0.2);
    border-radius: 2px;
    overflow: hidden;
    flex-shrink: 0;

    .progress-bar {
      width: 100%;
      height: 100%;
      background: linear-gradient(to right, #F27044, #E6B87D);
      animation: progress 1.5s ease-in-out infinite;
    }
  }
}

// 状态指示灯 - 立体发光
.status-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  transition: all 300ms ease;
}

@keyframes glow-occupied {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 12px rgba(217, 72, 54, 0.5);
  }
  50% {
    opacity: 0.7;
    box-shadow: 0 0 8px rgba(217, 72, 54, 0.3);
  }
}

@keyframes glow-cleaning {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 12px rgba(242, 112, 68, 0.4);
  }
  50% {
    opacity: 0.7;
    box-shadow: 0 0 8px rgba(242, 112, 68, 0.25);
  }
}

@keyframes progress {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(0); }
  100% { transform: translateX(100%); }
}
</style>