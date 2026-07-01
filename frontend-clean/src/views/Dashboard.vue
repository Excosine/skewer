<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import StatCard from '@/components/common/StatCard.vue'
import { getTables, getSkewerSales, getTableRevenue } from '@/api/admin'

const stats = ref([
  { label: '今日订单', value: 0, unit: '单' },
  { label: '今日签子', value: 0, unit: '支' },
  { label: '今日营收', value: 0, unit: '元' },
  { label: '在用桌台', value: 0, unit: '桌' }
])

const loading = ref(false)
const tableData = ref([])
const skewerSales = ref([])
const tableDistChart = ref(null)
const hotSalesChart = ref(null)

const fetchData = async () => {
  loading.value = true
  try {
    const today = new Date().toISOString().slice(0, 10)
    const [tables, skewers, revenue] = await Promise.all([
      getTables(),
      getSkewerSales(today),
      getTableRevenue(today)
    ])

    tableData.value = tables || []
    const skewerList = Array.isArray(skewers) ? skewers : []
    const tableList = Array.isArray(revenue) ? revenue : []

    const occupied = tables.filter(t => t.table_status === 1).length
    stats.value[3].value = `${occupied}/${tables.length}`
    const totalSkewers = skewerList.reduce((sum, s) => sum + (s.total_count || 0), 0)
    const totalRevenue = tableList.reduce((sum, t) => sum + (t.total_amount || 0), 0)
    stats.value[0].value = tableList.reduce((sum, t) => sum + (t.order_count || 0), 0)
    stats.value[1].value = totalSkewers
    stats.value[2].value = Number(totalRevenue).toFixed(2)

    skewerSales.value = [...skewerList].sort((a, b) => b.total_count - a.total_count).slice(0, 5)

    await nextTick()
    renderCharts()
  } catch { /* */ } finally {
    loading.value = false
  }
}

const renderCharts = () => {
  // 桌况分布饼图 - 火锅暖色风格
  if (tableDistChart.value) {
    const chart = echarts.init(tableDistChart.value)
    const free = tableData.value.filter(t => t.table_status === 0).length
    const busy = tableData.value.filter(t => t.table_status === 1).length
    const clean = tableData.value.filter(t => t.table_status === 2).length

    chart.setOption({
      tooltip: {
        trigger: 'item',
        backgroundColor: '#1A1512',
        borderColor: 'rgba(217, 72, 54, 0.3)',
        textStyle: { color: '#F8F5F2' }
      },
      legend: {
        bottom: 0,
        textStyle: { color: '#BFAFA6' }
      },
      series: [{
        type: 'pie',
        radius: ['45%', '72%'],
        center: ['50%', '45%'],
        label: {
          formatter: '{b}\n{c}桌',
          color: '#F8F5F2'
        },
        itemStyle: {
          borderColor: 'rgba(26, 21, 18, 0.6)',
          borderWidth: 2
        },
        data: [
          { value: busy, name: '占用', itemStyle: { color: '#D94836' } },
          { value: clean, name: '清洁中', itemStyle: { color: '#F27044' } },
          { value: free, name: '空闲', itemStyle: { color: '#6B5B53' } }
        ]
      }]
    })
  }

  // 热销排行柱状图 - 火锅暖色风格
  if (hotSalesChart.value) {
    const chart = echarts.init(hotSalesChart.value)
    const names = skewerSales.value.map(s => s.skewer_name)
    const counts = skewerSales.value.map(s => Number(s.total_count))
    const maxVal = Math.max(...counts, 1)

    chart.setOption({
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#1A1512',
        borderColor: 'rgba(217, 72, 54, 0.3)',
        textStyle: { color: '#F8F5F2' }
      },
      grid: { left: 10, right: 30, top: 10, bottom: 30, containLabel: true },
      xAxis: {
        type: 'category',
        data: names,
        axisLabel: {
          fontSize: 11,
          color: '#BFAFA6'
        },
        axisLine: { lineStyle: { color: 'rgba(248, 245, 242, 0.1)' } }
      },
      yAxis: {
        type: 'value',
        max: Math.ceil(maxVal * 1.2),
        minInterval: 1,
        axisLine: { lineStyle: { color: 'rgba(248, 245, 242, 0.1)' } },
        splitLine: { lineStyle: { color: 'rgba(248, 245, 242, 0.05)' } }
      },
      series: [{
        type: 'bar',
        data: counts,
        barWidth: '55%',
        itemStyle: {
          borderRadius: [6, 6, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#D94836' },
            { offset: 0.5, color: '#F27044' },
            { offset: 1, color: '#E6B87D' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: '#F27044',
            shadowBlur: 20,
            shadowColor: 'rgba(217, 72, 54, 0.3)'
          }
        }
      }]
    })
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <h1 class="page-title">仪表盘</h1>

    <!-- 统计卡片 -->
    <div class="stat-grid" v-loading="loading">
      <StatCard
        v-for="s in stats"
        :key="s.label"
        :label="s.label"
        :value="s.value"
        :unit="s.unit"
      />
    </div>

    <!-- 图表区域 -->
    <div class="charts-row">
      <!-- 桌况分布 -->
      <div class="chart-card">
        <h3 class="card-title">桌况分布</h3>
        <div ref="tableDistChart" class="chart-container" />
      </div>

      <!-- 今日热销 TOP5 -->
      <div class="chart-card">
        <h3 class="card-title">今日热销 TOP5</h3>
        <div v-if="skewerSales.length > 0" ref="hotSalesChart" class="chart-container" />
        <div v-else class="empty-tip">今日暂无已结账订单，热销榜待产生</div>
      </div>

      <!-- 快捷入口 -->
      <div class="quick-card">
        <h3 class="card-title">快捷入口</h3>

        <!-- 桌况概览 -->
        <div class="table-grid-scroll">
          <div
            v-for="t in tableData"
            :key="t.table_code"
            :class="['table-cell', `status-${t.table_status}`]"
          >
            <span class="cell-code">{{ t.table_code }}</span>
            <span class="cell-zone">{{ t.zone_name }}</span>
            <span class="cell-status">
              {{ t.table_status === 1 ? '占用' : t.table_status === 2 ? '清洁' : '空闲' }}
            </span>
          </div>
        </div>

        <!-- 快捷链接 -->
        <div class="quick-links">
          <router-link to="/monitor" class="link-item">
            <span>运营监控</span>
          </router-link>
          <router-link to="/prices" class="link-item">
            <span>价格管理</span>
          </router-link>
          <router-link to="/users" class="link-item">
            <span>员工管理</span>
          </router-link>
          <router-link to="/reports" class="link-item">
            <span>数据报表</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.dashboard {
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

  .stat-grid {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    flex-wrap: wrap;
  }
}

.charts-row {
  display: flex;
  gap: 20px;
}

.chart-card {
  flex: 1;
  min-width: 280px;
  background: rgba(26, 21, 18, 0.6);
  border: 1px solid rgba(248, 245, 242, 0.08);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(15, 12, 10, 0.3);
  position: relative;

  // 卡片顶部暖色点缀
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(217, 72, 54, 0.15), transparent);
  }

  .card-title {
    font-size: 14px;
    font-weight: 500;
    color: #BFAFA6;
    margin: 0 0 16px 0;
    letter-spacing: 1px;
  }

  .chart-container {
    width: 100%;
    height: 240px;
  }
}

.quick-card {
  min-width: 260px;
  background: rgba(26, 21, 18, 0.6);
  border: 1px solid rgba(248, 245, 242, 0.08);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(15, 12, 10, 0.3);
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(230, 184, 125, 0.15), transparent);
  }

  .card-title {
    font-size: 14px;
    font-weight: 500;
    color: #BFAFA6;
    margin: 0 0 16px 0;
    letter-spacing: 1px;
  }
}

.table-grid-scroll {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  max-height: 160px;
  overflow-y: auto;
  margin-bottom: 16px;
  padding-right: 4px;

  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(217, 72, 54, 0.3);
    border-radius: 2px;
  }
}

.table-cell {
  width: 60px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  flex-shrink: 0;
  transition: all 200ms ease;

  // 空闲状态 - 暖灰调
  &.status-0 {
    background: rgba(107, 91, 83, 0.2);
    border: 1px solid rgba(107, 91, 83, 0.3);
    color: #BFAFA6;
  }

  // 占用状态 - 牛油红
  &.status-1 {
    background: linear-gradient(135deg, rgba(217, 72, 54, 0.3), rgba(242, 112, 68, 0.2));
    border: 1px solid rgba(217, 72, 54, 0.4);
    color: #F8F5F2;
    box-shadow: 0 0 12px rgba(217, 72, 54, 0.2);
  }

  // 清洁中状态 - 烟火橙
  &.status-2 {
    background: linear-gradient(135deg, rgba(242, 112, 68, 0.25), rgba(230, 184, 125, 0.15));
    border: 1px solid rgba(242, 112, 68, 0.3);
    color: #F8F5F2;
    box-shadow: 0 0 8px rgba(242, 112, 68, 0.15);
  }

  .cell-code {
    font-weight: 600;
    font-size: 12px;
    font-family: 'SF Mono', 'Consolas', monospace;
  }

  .cell-zone {
    font-size: 9px;
    opacity: 0.7;
  }

  .cell-status {
    font-size: 9px;
    margin-top: 2px;
  }
}

.quick-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid rgba(248, 245, 242, 0.08);

  .link-item {
      display: flex;
      align-items: center;
      padding: 10px 16px;
      background: rgba(248, 245, 242, 0.04);
      border: 1px solid rgba(248, 245, 242, 0.08);
      border-radius: 8px;
      color: #BFAFA6;
      font-size: 13px;
      font-weight: 500;
      text-decoration: none;
      transition: all 250ms ease;
      letter-spacing: 1px;

      &:hover {
        background: rgba(242, 112, 68, 0.1);
        border-color: rgba(242, 112, 68, 0.2);
        color: #F8F5F2;
        transform: translateY(-2px);
      }
    }
}

.empty-tip {
  text-align: center;
  color: #BFAFA6;
  padding: 60px 20px;
  font-size: 13px;
  letter-spacing: 1px;
}
</style>