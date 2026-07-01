<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import * as echarts from 'echarts'
import { getSkewerSales, getTableRevenue } from '@/api/admin'

const _d2 = new Date(); _d2.setDate(_d2.getDate() - 1)
const date = ref(_d2.toISOString().slice(0, 10))
const skewerData = ref([])
const tableData = ref([])
const loading = ref(false)
const activeTab = ref('skewers')
const skewerChart = ref(null)

// 计算各桌数据的占比
const maxSkewers = computed(() => {
  if (tableData.value.length === 0) return 1
  return Math.max(...tableData.value.map(t => Number(t.total_skewers)), 1)
})

const maxAmount = computed(() => {
  if (tableData.value.length === 0) return 1
  return Math.max(...tableData.value.map(t => Number(t.total_amount)), 1)
})

// 按营业额排序的桌台数据
const sortedTables = computed(() => {
  return [...tableData.value].sort((a, b) => Number(b.total_amount) - Number(a.total_amount))
})

const fetchData = async () => {
  loading.value = true
  try {
    const [skewers, tables] = await Promise.all([
      getSkewerSales(date.value),
      getTableRevenue(date.value)
    ])
    skewerData.value = Array.isArray(skewers) ? skewers : []
    tableData.value = Array.isArray(tables) ? tables : []

    await nextTick()
    renderCharts()
  } catch {
    skewerData.value = []
    tableData.value = []
  } finally {
    loading.value = false
  }
}

const renderCharts = () => {
  // 签子销量柱状图 - 鎏金高级风格
  if (skewerChart.value && skewerData.value.length > 0) {
    const chart = echarts.init(skewerChart.value)
    const names = skewerData.value.map(s => s.skewer_name)
    const values = skewerData.value.map(s => Number(s.total_count))
    const maxVal = Math.max(...values, 1)

    chart.setOption({
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(26, 21, 18, 0.95)',
        borderColor: 'rgba(217, 72, 54, 0.3)',
        textStyle: { 
          color: '#F8F5F2',
          fontSize: 14,
          fontWeight: 600
        }
      },
      // 调整图表位置，增加顶部空间让纵坐标轴名显示清楚
      grid: { 
        left: 12, 
        right: 40, 
        top: 50,    // 增加顶部空间，让轴名显示清楚
        bottom: 80, 
        containLabel: true 
      },
      xAxis: {
        type: 'category',
        data: names,
        axisLabel: {
          rotate: 25,
          fontSize: 13,
          fontWeight: 600,
          color: '#E6B87D',       // 鎏金色
          letterSpacing: 1
        },
        axisLine: { 
          lineStyle: { 
            color: 'rgba(230, 184, 125, 0.2)',  // 鎏金边框
            width: 1
          } 
        },
        axisTick: {
          lineStyle: { color: 'rgba(230, 184, 125, 0.15)' }
        }
      },
      yAxis: {
        type: 'value',
        name: '销量(根)',
        nameTextStyle: {
          color: '#E6B87D',           // 鎏金色
          fontSize: 14,
          fontWeight: 700,
          letterSpacing: 2,
          padding: [0, 0, 8, 0]       // 增加底部间距
        },
        max: Math.ceil(maxVal * 1.2),
        axisLabel: {
          color: '#E6B87D',           // 鎏金色
          fontSize: 13,
          fontWeight: 600,
          fontFamily: 'SF Mono, Consolas, monospace'
        },
        axisLine: { 
          lineStyle: { 
            color: 'rgba(230, 184, 125, 0.2)',  // 鎏金边框
            width: 1
          } 
        },
        axisTick: {
          lineStyle: { color: 'rgba(230, 184, 125, 0.15)' }
        },
        splitLine: { 
          lineStyle: { 
            color: 'rgba(230, 184, 125, 0.08)',  // 鎏金淡线
            type: 'dashed'
          } 
        }
      },
      series: [{
        type: 'bar',
        name: '销量',
        data: values,
        itemStyle: {
          borderRadius: [6, 6, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#D94836' },    // 牛油红
            { offset: 0.5, color: '#F27044' },  // 烟火橙
            { offset: 1, color: '#E6B87D' }     // 焦糖金
          ])
        },
        barWidth: '50%',
        emphasis: {
          itemStyle: {
            color: '#F27044',
            shadowBlur: 20,
            shadowColor: 'rgba(217, 72, 54, 0.4)'
          }
        }
      }]
    })
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="reports-page">
    <!-- 页面标题 -->
    <h1 class="page-title">数据报表</h1>

    <!-- 日期选择器 -->
    <div class="filter-bar">
      <el-date-picker
        v-model="date"
        type="date"
        placeholder="选择日期"
        value-format="YYYY-MM-DD"
        @change="fetchData"
      />
      <el-button type="primary" @click="fetchData" class="query-btn">
        查询
      </el-button>
    </div>

    <!-- 标签页 -->
    <el-tabs v-model="activeTab">
      <!-- 销量统计 -->
      <el-tab-pane label="销量统计" name="skewers">
        <div class="chart-card">
          <div ref="skewerChart" class="chart-container" />
        </div>

        <el-table :data="skewerData" v-loading="loading" class="data-table">
          <el-table-column prop="skewer_name" label="签子名称" />
          <el-table-column prop="total_count" label="销量" width="100">
            <template #default="{ row }">
              <span class="data-value orange">{{ row.total_count }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="total_amount" label="营业额" width="120">
            <template #default="{ row }">
              <span class="data-value gold">¥{{ row.total_amount }}</span>
            </template>
          </el-table-column>
        </el-table>

        <div v-if="!loading && skewerData.length === 0" class="empty-state">
          该日期暂无数据，请选择其他日期
        </div>
      </el-tab-pane>

      <!-- 各桌营收 -->
      <el-tab-pane label="各桌营收" name="tables">
        <div class="table-grid" v-loading="loading">
          <div class="table-card" v-for="t in sortedTables" :key="t.table_code">
            <!-- 卡片头部 -->
            <div class="card-header">
              <span class="table-code">{{ t.table_code }}</span>
              <span class="zone-badge">{{ t.zone_name }}</span>
            </div>

            <!-- 数据统计 -->
            <div class="card-stats">
              <div class="stat-row">
                <div class="stat-item">
                  <span class="stat-label">订单数</span>
                  <span class="stat-value">{{ t.order_count }}</span>
                </div>
              </div>

              <!-- 签子数进度条 -->
              <div class="stat-row">
                <div class="stat-item">
                  <div class="stat-header">
                    <span class="stat-label">签子数</span>
                    <span class="stat-value hotpot">{{ t.total_skewers }}</span>
                  </div>
                  <div class="progress-bar">
                    <div
                      class="progress-fill hotpot"
                      :style="{ width: (Number(t.total_skewers) / maxSkewers * 100) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>

              <!-- 营业额进度条 -->
              <div class="stat-row">
                <div class="stat-item">
                  <div class="stat-header">
                    <span class="stat-label">营业额</span>
                    <span class="stat-value gold">¥{{ Number(t.total_amount).toFixed(2) }}</span>
                  </div>
                  <div class="progress-bar">
                    <div
                      class="progress-fill gold"
                      :style="{ width: (Number(t.total_amount) / maxAmount * 100) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!loading && tableData.length === 0" class="empty-state">
          该日期暂无数据，请选择其他日期
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped lang="scss">
.reports-page {
  // 页面标题 - 焦糖鎏金色渐变效果
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

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;

  .query-btn {
    height: 36px;
    padding: 0 20px;
    background: linear-gradient(135deg, #D94836, #F27044);
    border: none;
    border-radius: 9999px;
    font-weight: 500;
    letter-spacing: 1px;
  }
}

.chart-card {
  background: rgba(26, 21, 18, 0.6);
  border: 1px solid rgba(248, 245, 242, 0.08);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(15, 12, 10, 0.3);

  .chart-container {
    width: 100%;
    height: 320px;
  }
}

.data-table {
  .data-value {
    font-weight: 600;
    font-family: 'SF Mono', 'Consolas', monospace;

    &.orange { color: #F27044; }
    &.gold { color: #E6B87D; }
  }
}

// 各桌营收卡片网格
.table-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.table-card {
  background: rgba(26, 21, 18, 0.6);
  border: 1px solid rgba(248, 245, 242, 0.08);
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: 0 4px 24px rgba(15, 12, 10, 0.3);
  transition: all 250ms ease;
  position: relative;

  // 卡片边缘暖色点缀
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 12px;
    right: 12px;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(217, 72, 54, 0.2), transparent);
  }

  &:hover {
    transform: translateY(-4px);
    border-color: rgba(242, 112, 68, 0.15);
    box-shadow: 0 8px 32px rgba(242, 112, 68, 0.15);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(248, 245, 242, 0.08);

    .table-code {
      font-size: 18px;
      font-weight: 600;
      color: #F8F5F2;
      font-family: 'SF Mono', 'Consolas', monospace;
    }

    .zone-badge {
      font-size: 12px;
      color: #BFAFA6;
      padding: 4px 10px;
      background: rgba(248, 245, 242, 0.05);
      border-radius: 9999px;
    }
  }

  .card-stats {
    .stat-row {
      margin-bottom: 12px;

      &:last-child {
        margin-bottom: 0;
      }
    }

    .stat-item {
      .stat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
      }

      .stat-label {
        font-size: 12px;
        color: #BFAFA6;
        letter-spacing: 1px;
      }

      .stat-value {
        font-size: 14px;
        font-weight: 600;
        color: #F8F5F2;
        font-family: 'SF Mono', 'Consolas', monospace;

        &.hotpot { color: #D94836; }
        &.gold { color: #E6B87D; }
      }
    }
  }
}

// 进度条 - 火锅暖色柔光
.progress-bar {
  height: 6px;
  background: rgba(248, 245, 242, 0.05);
  border-radius: 3px;
  overflow: hidden;
  position: relative;

  .progress-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 350ms ease;
    position: relative;

    // 牛油红渐变
    &.hotpot {
      background: linear-gradient(90deg, #D94836, #F27044);
      box-shadow: 0 0 8px rgba(217, 72, 54, 0.3);
    }

    // 鎏金渐变
    &.gold {
      background: linear-gradient(90deg, #F27044, #E6B87D);
      box-shadow: 0 0 8px rgba(230, 184, 125, 0.3);
    }
  }
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #BFAFA6;
  font-size: 14px;
  letter-spacing: 1px;
}
</style>