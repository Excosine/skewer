<script setup>
import { ref, onMounted } from 'vue'
import { getLogs } from '@/api/log'

const logs = ref([])
const total = ref(0)
const loading = ref(false)
const date = ref(new Date().toISOString().slice(0, 10))
const currentPage = ref(1)
const pageSize = ref(20)

const operationTypeMap = {
  'price_adjust': '调价',
  'skewer_online': '上架签子',
  'skewer_offline': '下架签子',
  'user_create': '新增员工',
  'user_update': '编辑员工',
  'user_disable': '禁用员工',
  'user_enable': '启用员工',
  'order_close': '强制结账',
}

const getTagClass = (type) => {
  if (type === 'order_close') return 'danger'
  if (type === 'price_adjust') return 'warning'
  if (type.includes('user')) return 'user'
  return 'default'
}

const fetchLogs = async () => {
  loading.value = true
  try {
    const res = await getLogs({
      date: date.value,
      page: currentPage.value,
      page_size: pageSize.value
    })
    logs.value = res.logs || []
    total.value = res.total || 0
  } catch {
    logs.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

const onPageChange = (page) => {
  currentPage.value = page
  fetchLogs()
}

onMounted(fetchLogs)
</script>

<template>
  <div class="logs-page">
    <!-- 页面标题 - 鎏金效果 -->
    <h1 class="page-title">操作日志</h1>

    <!-- 筛选栏 - 鎏金按钮 -->
    <div class="filter-bar">
      <el-date-picker v-model="date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" class="date-picker" />
      <el-button type="primary" @click="fetchLogs" class="query-btn">查询</el-button>
    </div>

    <!-- 日志表格 - 鎏金高级风格 -->
    <div class="table-container">
      <el-table :data="logs" v-loading="loading" class="logs-table">
        <el-table-column prop="created_at" label="操作时间" width="180" align="center">
          <template #default="{ row }">
            <span class="time-text">{{ row.created_at?.slice(0, 19).replace('T', ' ') }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="real_name" label="操作人" width="120" align="center">
          <template #default="{ row }">
            <span class="name-text">{{ row.real_name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="operation_type" label="操作类型" width="140" align="center">
          <template #default="{ row }">
            <div class="type-tag" :class="getTagClass(row.operation_type)">
              {{ operationTypeMap[row.operation_type] || row.operation_type }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="target_name" label="操作对象" width="160" align="center">
          <template #default="{ row }">
            <span class="target-text">{{ row.target_name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="detail" label="详情" min-width="200" align="center">
          <template #default="{ row }">
            <span class="detail-text">{{ row.detail }}</span>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态提示 -->
      <div v-if="!loading && logs.length === 0" class="empty-state">
        暂无操作日志
      </div>
    </div>

    <!-- 分页区域 - 鎏金风格 -->
    <div v-if="total > pageSize" class="pagination-area">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="onPageChange"
        class="gold-pagination"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.logs-page {
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

// 筛选栏 - 鎏金风格
.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;

  .date-picker {
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
        letter-spacing: 1px;

        &::placeholder {
          color: #6B5B52;
        }
      }
    }
  }

  .query-btn {
    background: linear-gradient(135deg, #D94836, #F27044);
    border: none;
    border-radius: 9999px;
    font-weight: 600;
    letter-spacing: 2px;
    box-shadow: 0 4px 16px rgba(217, 72, 54, 0.25);
    transition: all 300ms ease;

    &:hover {
      box-shadow: 0 6px 24px rgba(217, 72, 54, 0.35);
      transform: translateY(-2px);
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
.logs-table {
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
.time-text {
  font-size: 14px;
  font-weight: 500;
  font-family: 'SF Mono', 'Consolas', monospace;
  color: #BFAFA6;
  letter-spacing: 1px;
}

.name-text {
  font-size: 15px;
  font-weight: 600;
  color: #E6B87D;
  text-shadow: 0 0 8px rgba(230, 184, 125, 0.3);
  letter-spacing: 2px;
}

.target-text {
  font-size: 14px;
  font-weight: 500;
  color: #F8F5F2;
  letter-spacing: 1px;
}

.detail-text {
  font-size: 13px;
  font-weight: 500;
  color: #BFAFA6;
  letter-spacing: 1px;
}

// 操作类型标签 - 鎏金风格
.type-tag {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  &.danger {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #EF4444;
    text-shadow: 0 0 6px rgba(239, 68, 68, 0.3);
  }

  &.warning {
    background: rgba(242, 112, 68, 0.15);
    border: 1px solid rgba(242, 112, 68, 0.3);
    color: #F27044;
    text-shadow: 0 0 6px rgba(242, 112, 68, 0.3);
  }

  &.user {
    background: rgba(217, 72, 54, 0.15);
    border: 1px solid rgba(217, 72, 54, 0.3);
    color: #D94836;
    text-shadow: 0 0 6px rgba(217, 72, 54, 0.3);
  }

  &.default {
    background: rgba(230, 184, 125, 0.1);
    border: 1px solid rgba(230, 184, 125, 0.2);
    color: #E6B87D;
    text-shadow: 0 0 6px rgba(230, 184, 125, 0.2);
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

// 分页区域 - 鎏金风格
.pagination-area {
  margin-top: 24px;
  display: flex;
  justify-content: center;

  .gold-pagination {
    :deep(.el-pagination) {
      .btn-prev, .btn-next {
        background: rgba(26, 21, 18, 0.4);
        border: 1px solid rgba(230, 184, 125, 0.15);
        color: #E6B87D;
        font-weight: 600;
        border-radius: 8px;
        transition: all 250ms ease;

        &:hover {
          background: rgba(230, 184, 125, 0.1);
          border-color: rgba(230, 184, 125, 0.25);
          color: #F8F5F2;
        }

        &:disabled {
          color: #6B5B52;
          border-color: rgba(230, 184, 125, 0.08);
        }
      }

      .el-pager li {
        background: rgba(26, 21, 18, 0.4);
        border: 1px solid rgba(230, 184, 125, 0.15);
        color: #E6B87D;
        font-weight: 600;
        font-family: 'SF Mono', 'Consolas', monospace;
        border-radius: 8px;
        margin: 0 4px;
        transition: all 250ms ease;

        &:hover {
          background: rgba(230, 184, 125, 0.1);
          border-color: rgba(230, 184, 125, 0.25);
          color: #F8F5F2;
        }

        &.is-active {
          background: linear-gradient(135deg, #D94836, #F27044);
          border-color: transparent;
          color: #F8F5F2;
          box-shadow: 0 4px 12px rgba(217, 72, 54, 0.2);
        }
      }
    }
  }
}
</style>