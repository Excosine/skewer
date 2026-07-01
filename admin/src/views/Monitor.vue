<script setup>
import { ref, computed, onMounted } from 'vue'
import TableCard from '@/components/common/TableCard.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTables, getOrderDetail, closeOrder, resetTable } from '@/api/admin'

const tables = ref([])
const loading = ref(false)

const selectedZone = ref('all')
const zones = computed(() => {
  const s = new Set(tables.value.map(t => t.zone_name))
  return Array.from(s)
})

const filteredTables = computed(() => {
  if (selectedZone.value === 'all') return tables.value
  return tables.value.filter(t => t.zone_name === selectedZone.value)
})

const orderDialogVisible = ref(false)
const currentOrder = ref(null)
const orderLoading = ref(false)

const fetchTables = async () => {
  loading.value = true
  try {
    tables.value = await getTables()
  } catch { /* */ } finally {
    loading.value = false
  }
}

const handleTableClick = async (table) => {
  if (table.table_status === 0) return ElMessage.info('该桌空闲，无订单')
  if (table.table_status === 2) return ElMessage.info('该桌清洁中')
  if (!table.order_id) return

  orderLoading.value = true
  try {
    const order = await getOrderDetail(table.order_id)
    order.table_code = table.table_code
    order.waiter_name = table.waiter_name
    currentOrder.value = order
    orderDialogVisible.value = true
  } catch {
    ElMessage.error('获取订单详情失败')
  } finally {
    orderLoading.value = false
  }
}

const handleCloseOrder = async () => {
  try {
    await ElMessageBox.confirm('确定要强制结账吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const tableCode = currentOrder.value.table_code
    await closeOrder(currentOrder.value.id)
    ElMessage.success('已结账，15秒后自动恢复为空闲')
    orderDialogVisible.value = false
    fetchTables()

    // 15 秒后自动将桌子从"清洁中"恢复为"空闲"
    setTimeout(async () => {
      try {
        await resetTable(tableCode)
        fetchTables()
      } catch { /* */ }
    }, 15000)
  } catch { /* */ }
}

onMounted(fetchTables)
</script>

<template>
  <div class="monitor-page">
    <!-- 页面标题 - 鎏金效果 -->
    <h1 class="page-title">运营监控</h1>

    <!-- 区域筛选栏 - 鎏金高级风格 -->
    <div class="filter-bar">
      <div class="filter-label">区域筛选</div>
      <el-radio-group v-model="selectedZone" class="zone-radio">
        <el-radio-button value="all">全部区域</el-radio-button>
        <el-radio-button v-for="z in zones" :key="z" :value="z">{{ z }}</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 统计信息卡片 - 鎏金立体效果 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-glow"></div>
        <div class="stat-content">
          <div class="stat-tag">总桌数</div>
          <div class="stat-value">{{ filteredTables.length }}</div>
        </div>
      </div>
      <div class="stat-card active">
        <div class="stat-glow"></div>
        <div class="stat-content">
          <div class="stat-tag">占用桌</div>
          <div class="stat-value">{{ filteredTables.filter(t => t.table_status === 1).length }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-glow"></div>
        <div class="stat-content">
          <div class="stat-tag">空闲桌</div>
          <div class="stat-value">{{ filteredTables.filter(t => t.table_status === 0).length }}</div>
        </div>
      </div>
      <div class="stat-card cleaning">
        <div class="stat-glow"></div>
        <div class="stat-content">
          <div class="stat-tag">清洁桌</div>
          <div class="stat-value">{{ filteredTables.filter(t => t.table_status === 2).length }}</div>
        </div>
      </div>
    </div>

    <!-- 桌台网格 - 更大间距 -->
    <div v-loading="loading" class="tables-grid">
      <TableCard
        v-for="t in filteredTables"
        :key="t.table_code"
        :table-code="t.table_code"
        :status="t.table_status"
        :total-count="t.total_count || 0"
        :total-price="t.total_price || 0"
        @click="handleTableClick(t)"
      />
    </div>

    <!-- 状态说明 - 鎏金高级风格 -->
    <div class="status-legend">
      <div class="legend-title">状态说明</div>
      <div class="legend-items">
        <div class="legend-item idle">
          <div class="legend-dot"></div>
          <span>空闲可用</span>
        </div>
        <div class="legend-item occupied">
          <div class="legend-dot"></div>
          <span>正在占用</span>
        </div>
        <div class="legend-item cleaning">
          <div class="legend-dot"></div>
          <span>清洁整理</span>
        </div>
      </div>
    </div>

    <!-- 订单详情弹窗 -->
    <el-dialog v-model="orderDialogVisible" title="订单详情" width="560px" class="order-dialog">
      <div v-if="currentOrder" v-loading="orderLoading">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单编号">{{ currentOrder.order_no }}</el-descriptions-item>
          <el-descriptions-item label="桌号">{{ currentOrder.table_code }}</el-descriptions-item>
          <el-descriptions-item label="服务员">{{ currentOrder.waiter_name }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ currentOrder.created_at }}</el-descriptions-item>
        </el-descriptions>

        <div class="order-items">
          <h3 class="items-title">签子明细</h3>
          <el-table :data="currentOrder.items" border size="small">
            <el-table-column prop="skewer_name" label="签子名称" />
            <el-table-column prop="count" label="数量" width="80" />
            <el-table-column label="单价" width="80">
              <template #default="{ row }">¥{{ row.unit_price }}</template>
            </el-table-column>
            <el-table-column label="小计" width="100">
              <template #default="{ row }">
                <span class="subtotal-text">¥{{ row.subtotal }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="order-total">
          <span class="total-label">区域加价:</span>
          <span class="total-surcharge">¥{{ currentOrder.zone_surcharge }}</span>
          <span class="total-divider"></span>
          <span class="total-label">总计:</span>
          <span class="total-amount">¥{{ currentOrder.total_price }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="orderDialogVisible = false">关闭</el-button>
        <el-button type="danger" @click="handleCloseOrder">强制结账</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.monitor-page {
  // 页面标题 - 鎏金效果
  .page-title {
    font-size: 28px;
    font-weight: 700;
    color: #E6B87D;
    margin-bottom: 32px;
    letter-spacing: 3px;
    text-shadow: 0 0 20px rgba(230, 184, 125, 0.4);
    position: relative;

    &::after {
      content: '';
      position: absolute;
      bottom: -8px;
      left: 0;
      width: 120px;
      height: 3px;
      background: linear-gradient(to right, #D94836, #E6B87D);
      border-radius: 2px;
    }
  }
}

// 区域筛选栏 - 鎏金风格
.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;

  .filter-label {
    font-size: 15px;
    font-weight: 600;
    color: #E6B87D;
    letter-spacing: 2px;
    text-shadow: 0 0 8px rgba(230, 184, 125, 0.2);
  }

  .zone-radio {
    :deep(.el-radio-button__inner) {
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 500;
      background: rgba(26, 21, 18, 0.4);
      border: 1px solid rgba(248, 245, 242, 0.12);
      color: #BFAFA6;
      transition: all 250ms ease;

      &:hover {
        background: rgba(242, 112, 68, 0.1);
        border-color: rgba(242, 112, 68, 0.2);
        color: #F8F5F2;
      }
    }

    :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
      background: linear-gradient(135deg, rgba(217, 72, 54, 0.2), rgba(242, 112, 68, 0.15));
      border-color: rgba(217, 72, 54, 0.4);
      color: #E6B87D;
      box-shadow: 0 0 16px rgba(217, 72, 54, 0.2);
    }
  }
}

// 统计卡片 - 鎏金立体效果，垂直居中对齐布局
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;

  .stat-card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    // 统一内边距
    padding: 24px;
    background: rgba(26, 21, 18, 0.5);
    border: 1px solid rgba(248, 245, 242, 0.1);
    border-radius: 16px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(15, 12, 10, 0.2);
    transition: all 300ms ease;
    box-sizing: border-box;
    min-height: 140px;

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(15, 12, 10, 0.3);
      border-color: rgba(230, 184, 125, 0.15);
    }

    // 内部光晕
    .stat-glow {
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at center, rgba(230, 184, 125, 0.05) 0%, transparent 70%);
      pointer-events: none;
    }

    // 内容容器 - 垂直居中布局，固定间距
    .stat-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      // 固定上下间距
      gap: 16px;
      width: 100%;
      z-index: 1;

      // 顶部小字框 - 固定尺寸和居中
      .stat-tag {
        width: 72px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 600;
        color: #E6B87D;
        background: rgba(230, 184, 125, 0.08);
        border: 1px solid rgba(230, 184, 125, 0.15);
        border-radius: 8px;
        text-shadow: 0 0 8px rgba(230, 184, 125, 0.3);
        letter-spacing: 2px;
        flex-shrink: 0;
      }

      // 中间数字 - 固定高度确保对齐
      .stat-value {
        font-size: 36px;
        font-weight: 700;
        color: #E6B87D;
        font-family: 'SF Mono', 'Consolas', monospace;
        text-shadow: 0 0 12px rgba(230, 184, 125, 0.3);
        // 固定高度确保四个卡片位置完全平齐
        height: 40px;
        line-height: 40px;
        flex-shrink: 0;
      }
    }

    // 占用状态特殊样式
    &.active {
      background: linear-gradient(135deg, rgba(217, 72, 54, 0.12), rgba(242, 112, 68, 0.08));
      border-color: rgba(217, 72, 54, 0.2);

      .stat-content .stat-tag {
        background: rgba(217, 72, 54, 0.15);
        border-color: rgba(217, 72, 54, 0.3);
        color: #D94836;
        text-shadow: 0 0 8px rgba(217, 72, 54, 0.4);
      }

      .stat-content .stat-value {
        color: #D94836;
        text-shadow: 0 0 12px rgba(217, 72, 54, 0.4);
      }
    }

    // 清洁状态特殊样式
    &.cleaning {
      background: linear-gradient(135deg, rgba(242, 112, 68, 0.1), rgba(230, 184, 125, 0.06));
      border-color: rgba(242, 112, 68, 0.15);

      .stat-content .stat-tag {
        background: rgba(242, 112, 68, 0.12);
        border-color: rgba(242, 112, 68, 0.25);
        color: #F27044;
        text-shadow: 0 0 8px rgba(242, 112, 68, 0.3);
      }

      .stat-content .stat-value {
        color: #F27044;
        text-shadow: 0 0 12px rgba(242, 112, 68, 0.3);
      }
    }
  }
}

// 桌台网格 - 更大间距
.tables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 24px;
  padding: 8px;
}

// 状态说明 - 鎏金高级风格
.status-legend {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-top: 32px;
  padding: 20px 28px;
  background: rgba(26, 21, 18, 0.4);
  border: 1px solid rgba(248, 245, 242, 0.08);
  border-radius: 16px;
  position: relative;

  // 顶部鎏金装饰
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 28px;
    right: 28px;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(230, 184, 125, 0.2), transparent);
  }

  .legend-title {
    font-size: 15px;
    font-weight: 600;
    color: #E6B87D;
    letter-spacing: 2px;
    text-shadow: 0 0 8px rgba(230, 184, 125, 0.2);
  }

  .legend-items {
    display: flex;
    gap: 16px;

    .legend-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 18px;
      border-radius: 10px;
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 1px;
      transition: all 250ms ease;

      .legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        box-shadow: 0 0 8px currentColor;
      }

      &.idle {
        background: rgba(107, 91, 83, 0.25);
        border: 1px solid rgba(107, 91, 83, 0.35);
        color: #BFAFA6;

        .legend-dot {
          background: #BFAFA6;
        }

        &:hover {
          background: rgba(107, 91, 83, 0.35);
          transform: translateY(-2px);
        }
      }

      &.occupied {
        background: rgba(217, 72, 54, 0.15);
        border: 1px solid rgba(217, 72, 54, 0.3);
        color: #D94836;

        .legend-dot {
          background: #D94836;
          animation: pulse-occupied 2s ease-in-out infinite;
        }

        &:hover {
          background: rgba(217, 72, 54, 0.25);
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(217, 72, 54, 0.2);
        }
      }

      &.cleaning {
        background: rgba(242, 112, 68, 0.12);
        border: 1px solid rgba(242, 112, 68, 0.25);
        color: #F27044;

        .legend-dot {
          background: #F27044;
          animation: pulse-cleaning 2s ease-in-out infinite;
        }

        &:hover {
          background: rgba(242, 112, 68, 0.2);
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(242, 112, 68, 0.15);
        }
      }
    }
  }
}

@keyframes pulse-occupied {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(217, 72, 54, 0.5); }
  50% { opacity: 0.7; box-shadow: 0 0 6px rgba(217, 72, 54, 0.3); }
}

@keyframes pulse-cleaning {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(242, 112, 68, 0.4); }
  50% { opacity: 0.7; box-shadow: 0 0 6px rgba(242, 112, 68, 0.25); }
}

// 订单详情样式
.order-items {
  margin-top: 20px;

  .items-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 16px;
    color: #E6B87D;
    letter-spacing: 2px;
  }

  .subtotal-text {
    color: #D94836;
    font-weight: 600;
  }
}

.order-total {
  margin-top: 20px;
  padding: 20px 24px;
  background: linear-gradient(135deg, rgba(217, 72, 54, 0.1), rgba(242, 112, 68, 0.06));
  border: 1px solid rgba(217, 72, 54, 0.2);
  border-radius: 16px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;

  .total-label {
    font-size: 14px;
    color: #BFAFA6;
    letter-spacing: 1px;
  }

  .total-surcharge {
    font-size: 16px;
    color: #F8F5F2;
    font-weight: 500;
  }

  .total-divider {
    width: 24px;
    height: 1px;
    background: rgba(248, 245, 242, 0.1);
    margin: 0 8px;
  }

  .total-amount {
    font-size: 24px;
    font-weight: 700;
    color: #D94836;
    text-shadow: 0 0 12px rgba(217, 72, 54, 0.3);
  }
}
</style>