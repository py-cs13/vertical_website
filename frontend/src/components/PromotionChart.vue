<template>
  <div class="promotion-chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// 注册Chart.js组件
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

// 定义组件属性
const props = defineProps({
  // 图表类型：bar（柱状图）或 line（折线图）
  chartType: {
    type: String,
    default: 'bar',
    validator: (value) => ['bar', 'line'].includes(value)
  },
  // 图表标题
  title: {
    type: String,
    default: ''
  },
  // 图表数据
  chartData: {
    type: Object,
    required: true,
    default: () => ({
      labels: [],
      datasets: []
    })
  },
  // 图表配置选项
  options: {
    type: Object,
    default: () => ({})
  }
})

const chartCanvas = ref(null)
let chartInstance = null

// 创建图表实例
const createChart = () => {
  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')
  
  // 如果图表实例已存在，先销毁
  if (chartInstance) {
    chartInstance.destroy()
  }

  // 合并默认配置和用户配置
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: props.title !== '',
        text: props.title,
        font: {
          size: 16,
          weight: 'bold'
        },
        padding: {
          top: 10,
          bottom: 20
        }
      },
      legend: {
        position: 'top'
      },
      tooltip: {
        mode: 'index',
        intersect: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        },
        ticks: {
          callback: function(value) {
            // 处理大额数字，显示为k或M
            if (value >= 1000000) {
              return (value / 1000000).toFixed(1) + 'M'
            } else if (value >= 1000) {
              return (value / 1000).toFixed(1) + 'k'
            }
            return value
          }
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    },
    elements: {
      point: {
        radius: 4,
        hoverRadius: 6
      },
      line: {
        tension: 0.4
      }
    }
  }

  // 合并配置
  const mergedOptions = { ...defaultOptions, ...props.options }

  // 创建新的图表实例
  chartInstance = new ChartJS(ctx, {
    type: props.chartType,
    data: props.chartData,
    options: mergedOptions
  })
}

// 更新图表数据
const updateChart = () => {
  if (!chartInstance) return

  chartInstance.data = props.chartData
  chartInstance.update()
}

// 监听数据变化
watch(
  () => props.chartData,
  () => {
    updateChart()
  },
  { deep: true }
)

// 监听图表类型变化
watch(
  () => props.chartType,
  () => {
    createChart()
  }
)

// 组件挂载时创建图表
onMounted(() => {
  createChart()
})

// 组件卸载时销毁图表
onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>

<style scoped>
.promotion-chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>