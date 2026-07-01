<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSkewers, adjustPrice } from '@/api/admin'

const skewers = ref([])
const loading = ref(false)

const priceDialogVisible = ref(false)
const currentSkewer = ref(null)
const newPrice = ref(0)

const fetchSkewers = async () => {
  loading.value = true
  try {
    skewers.value = await getSkewers()
  } catch {
    // 已处理
  } finally {
    loading.value = false
  }
}

const handleAdjustPrice = (row) => {
  currentSkewer.value = row
  newPrice.value = row.unit_price
  priceDialogVisible.value = true
}

const handleSavePrice = async () => {
  try {
    await ElMessageBox.confirm(
      `确定将 "${currentSkewer.value.skewer_name}" 从 ¥${currentSkewer.value.unit_price} 调整为 ¥${newPrice.value}？`,
      '确认调价',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    await adjustPrice(currentSkewer.value.id, Number(newPrice.value))
    ElMessage.success('已调价')
    priceDialogVisible.value = false
    fetchSkewers()
  } catch {
    // 取消或错误
  }
}

onMounted(fetchSkewers)
</script>

<template>
  <div class="prices-page">
    <!-- 页面标题 - 鎏金效果 -->
    <h1 class="page-title">价格管理</h1>

    <!-- 操作栏 - 鎏金按钮 -->
    <div class="action-bar">
      <el-button @click="fetchSkewers" class="refresh-btn">
        刷新数据
      </el-button>
    </div>

    <!-- 价格表格 - 鎏金高级风格 -->
    <div class="table-container">
      <el-table :data="skewers" v-loading="loading" class="prices-table">
        <el-table-column prop="id" label="编号" width="80" align="center">
          <template #default="{ row }">
            <span class="table-id">{{ row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="skewer_name" label="名称" width="160" align="center">
          <template #default="{ row }">
            <span class="table-name">{{ row.skewer_name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="category_name" label="类别" width="120" align="center">
          <template #default="{ row }">
            <div class="category-tag">
              {{ row.category_name || '-' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="unit_price" label="当前价格" width="140" align="center">
          <template #default="{ row }">
            <span class="price-value">¥{{ row.unit_price }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default>
            <div class="status-tag active">
              在售
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" align="center">
          <template #default="{ row }">
            <el-button size="small" @click="handleAdjustPrice(row)" class="adjust-btn">
              调价
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态提示 -->
      <div v-if="!loading && skewers.length === 0" class="empty-state">
        暂无签子价格数据
      </div>
    </div>

    <!-- 调价弹窗 - 鎏金高级风格 -->
    <el-dialog v-model="priceDialogVisible" title="调整价格" width="380px" class="price-dialog">
      <div class="price-info">
        <div class="skewer-name">{{ currentSkewer?.skewer_name }}</div>
        <div class="current-price">
          当前价格: <span class="price-number">¥{{ currentSkewer?.unit_price }}</span>
        </div>
      </div>
      <el-form label-width="80px" class="price-form">
        <el-form-item label="新价格">
          <div class="price-input-wrapper">
            <el-input-number v-model="newPrice" :min="0" :precision="2" :step="0.5" class="price-input" />
            <span class="new-price-display">¥{{ newPrice }}</span>
          </div>
        </el-form-item>
        <el-form-item>
          <div class="price-hint">调价后仅影响新订单，历史订单价格不变</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="priceDialogVisible = false" class="cancel-btn">取消</el-button>
          <el-button type="primary" @click="handleSavePrice" class="save-btn">确认调价</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.prices-page {
  // 页面标题 - 鎏金效果
  .page-title {
    font-size: 28px;
    font-weight: 700;
    color: #E6B87D;
    margin-bottom: 32px;
    letter-spacing: 3px;
    text-shadow: 0 0 20px rgba(230, 184, 125, 0.4);
    position: relative;

    // 标题下方暖色装饰线
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

// 操作栏 - 鎏金按钮
.action-bar {
  margin-bottom: 24px;

  .refresh-btn {
    background: rgba(230, 184, 125, 0.08);
    border: 1px solid rgba(230, 184, 125, 0.15);
    border-radius: 9999px;
    color: #E6B87D;
    font-weight: 600;
    letter-spacing: 2px;
    transition: all 300ms ease;
    text-shadow: 0 0 6px rgba(230, 184, 125, 0.2);

    &:hover {
      background: rgba(230, 184, 125, 0.15);
      border-color: rgba(230, 184, 125, 0.25);
      color: #F8F5F2;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(230, 184, 125, 0.15);
    }
  }
}

// 表格容器 - 鎏金高级风格
.table-container {
  background: rgba(26, 21, 18, 0.4);
  border: 1px solid rgba(230, 184, 125, 0.15);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(15, 12, 10, 0.2);
  position: relative;

  // 顶部鎏金装饰线
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20px;
    right: 20px;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(230, 184, 125, 0.3), transparent);
  }
}

// 表格样式 - 鎏金高级风格
.prices-table {
  background: transparent;
  border-radius: 12px;

  :deep(.el-table__header-wrapper) {
    th {
      background: rgba(26, 21, 18, 0.3);
      border-color: rgba(230, 184, 125, 0.15);

      .cell {
        font-size: 15px;
        font-weight: 600;
        color: #E6B87D;
        letter-spacing: 2px;
        text-shadow: 0 0 8px rgba(230, 184, 125, 0.2);
      }
    }
  }

  :deep(.el-table__body-wrapper) {
    tr {
      background: rgba(26, 21, 18, 0.15);
      border-color: rgba(230, 184, 125, 0.1);

      &:hover > td {
        background: rgba(242, 112, 68, 0.08);
      }

      td {
        border-color: rgba(230, 184, 125, 0.1);
      }
    }
  }
}

// 表格内文字样式 - 鎏金高级感
.table-id {
  font-size: 14px;
  font-weight: 600;
  font-family: 'SF Mono', 'Consolas', monospace;
  color: #E6B87D;
  text-shadow: 0 0 6px rgba(230, 184, 125, 0.2);
}

.table-name {
  font-size: 15px;
  font-weight: 600;
  color: #E6B87D;
  text-shadow: 0 0 8px rgba(230, 184, 125, 0.3);
  letter-spacing: 2px;
}

// 类别标签 - 鎏金风格
.category-tag {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(230, 184, 125, 0.1);
  border: 1px solid rgba(230, 184, 125, 0.2);
  color: #E6B87D;
  text-shadow: 0 0 6px rgba(230, 184, 125, 0.2);
}

// 价格数值 - 牛油红发光效果
.price-value {
  font-size: 18px;
  font-weight: 700;
  font-family: 'SF Mono', 'Consolas', monospace;
  color: #D94836;
  text-shadow: 0 0 10px rgba(217, 72, 54, 0.4);
  letter-spacing: 1px;
}

// 状态标签 - 鎏金风格
.status-tag {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  &.active {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #22C55E;
    text-shadow: 0 0 6px rgba(34, 197, 94, 0.3);
  }
}

// 调价按钮 - 鎏金风格
.adjust-btn {
  background: rgba(217, 72, 54, 0.08);
  border: 1px solid rgba(217, 72, 54, 0.15);
  color: #D94836;
  font-weight: 600;
  letter-spacing: 1px;
  border-radius: 6px;
  transition: all 250ms ease;
  text-shadow: 0 0 6px rgba(217, 72, 54, 0.2);

  &:hover {
    background: rgba(217, 72, 54, 0.15);
    border-color: rgba(217, 72, 54, 0.25);
    color: #F8F5F2;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(217, 72, 54, 0.15);
  }
}

// 空状态提示
.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #BFAFA6;
  font-size: 15px;
  letter-spacing: 2px;
  font-weight: 500;
}

// 弹窗样式 - 鎏金高级风格
.price-dialog {
  :deep(.el-dialog) {
    background: rgba(26, 21, 18, 0.95);
    border: 1px solid rgba(230, 184, 125, 0.2);
    border-radius: 16px;
    box-shadow: 0 16px 48px rgba(15, 12, 10, 0.4);

    .el-dialog__header {
      background: linear-gradient(135deg, rgba(217, 72, 54, 0.1), rgba(230, 184, 125, 0.06));
      border-bottom: 1px solid rgba(230, 184, 125, 0.15);
      padding: 20px 24px;

      .el-dialog__title {
        font-size: 18px;
        font-weight: 700;
        color: #E6B87D;
        letter-spacing: 3px;
        text-shadow: 0 0 12px rgba(230, 184, 125, 0.3);
      }
    }

    .el-dialog__body {
      padding: 24px;
    }
  }
}

// 价格信息区域 - 鎏金风格
.price-info {
  padding: 20px;
  background: rgba(26, 21, 18, 0.3);
  border: 1px solid rgba(230, 184, 125, 0.15);
  border-radius: 12px;
  margin-bottom: 20px;

  .skewer-name {
    font-size: 18px;
    font-weight: 700;
    color: #E6B87D;
    letter-spacing: 3px;
    text-shadow: 0 0 12px rgba(230, 184, 125, 0.3);
    margin-bottom: 12px;
  }

  .current-price {
    font-size: 15px;
    color: #BFAFA6;
    letter-spacing: 2px;

    .price-number {
      font-size: 20px;
      font-weight: 700;
      font-family: 'SF Mono', 'Consolas', monospace;
      color: #D94836;
      text-shadow: 0 0 10px rgba(217, 72, 54, 0.4);
      margin-left: 8px;
    }
  }
}

// 表单样式 - 鎏金风格
.price-form {
  :deep(.el-form-item__label) {
    font-size: 14px;
    font-weight: 600;
    color: #E6B87D;
    letter-spacing: 2px;
    text-shadow: 0 0 6px rgba(230, 184, 125, 0.2);
  }

  .price-input-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;

    .price-input {
      width: 150px;

      :deep(.el-input__wrapper) {
        background: rgba(26, 21, 18, 0.4);
        border: 1px solid rgba(230, 184, 125, 0.15);
        border-radius: 8px;
        box-shadow: none;

        &:hover {
          border-color: rgba(230, 184, 125, 0.25);
        }

        &.is-focus {
          border-color: rgba(217, 72, 54, 0.3);
          box-shadow: 0 0 12px rgba(217, 72, 54, 0.15);
        }

        .el-input__inner {
          color: #F8F5F2;
          font-size: 14px;
          font-weight: 600;
          letter-spacing: 1px;
        }
      }
    }

    .new-price-display {
      font-size: 18px;
      font-weight: 700;
      font-family: 'SF Mono', 'Consolas', monospace;
      color: #D94836;
      text-shadow: 0 0 10px rgba(217, 72, 54, 0.4);
      letter-spacing: 1px;
    }
  }

  .price-hint {
    font-size: 13px;
    color: #F27044;
    letter-spacing: 1px;
    font-weight: 500;
    text-shadow: 0 0 6px rgba(242, 112, 68, 0.2);
  }
}

// 弹窗底部按钮 - 鎏金风格
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;

  .cancel-btn {
    background: rgba(26, 21, 18, 0.4);
    border: 1px solid rgba(230, 184, 125, 0.15);
    color: #BFAFA6;
    font-weight: 500;
    letter-spacing: 1px;
    border-radius: 8px;
    transition: all 250ms ease;

    &:hover {
      background: rgba(26, 21, 18, 0.6);
      border-color: rgba(230, 184, 125, 0.25);
      color: #F8F5F2;
    }
  }

  .save-btn {
    background: linear-gradient(135deg, #D94836, #F27044);
    border: none;
    font-weight: 600;
    letter-spacing: 2px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(217, 72, 54, 0.2);
    transition: all 250ms ease;

    &:hover {
      box-shadow: 0 6px 16px rgba(217, 72, 54, 0.3);
      transform: translateY(-1px);
    }
  }
}
</style>