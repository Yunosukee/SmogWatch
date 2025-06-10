<template>
  <div class="sparkline-container" ref="container">
    <canvas ref="sparklineCanvas" @mousemove="onMouseMove" @mouseleave="onMouseLeave"></canvas>
    <div v-if="tooltip.visible" class="tooltip" :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }">
      <div class="tooltip-content">
        <div class="tooltip-value">{{ tooltip.value }}</div>
        <div class="tooltip-time">{{ tooltip.time }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SparklineChart',
  props: {
    data: {
      type: Array,
      required: true
    },
    height: {
      type: Number,
      default: 40
    },
    color: {
      type: String,
      default: '#667eea'
    }
  },
  data() {
    return {
      validData: [],
      points: [],
      tooltip: {
        visible: false,
        x: 0,
        y: 0,
        value: '',
        time: ''
      }
    }
  },
  mounted() {
    this.drawSparkline()
  },
  watch: {
    data: {
      handler() {
        this.drawSparkline()
      },
      deep: true
    }
  },
  methods: {
    drawSparkline() {
      const canvas = this.$refs.sparklineCanvas
      if (!canvas) return
      
      const container = this.$refs.container
      const width = container.clientWidth
      const height = this.height
      
      // Set canvas size
      canvas.width = width
      canvas.height = height
      
      const ctx = canvas.getContext('2d')
      
      // Clear canvas
      ctx.clearRect(0, 0, width, height)
      
      if (!this.data || this.data.length < 2) return
      
      // Filter valid data points
      this.validData = this.data
        .filter(point => point.value !== null && point.value !== undefined)
        .slice(-10) // Take last 10 readings
      
      if (this.validData.length < 2) return
      
      // Get data range
      const values = this.validData.map(point => point.value)
      const minValue = Math.min(...values)
      const maxValue = Math.max(...values)
      const range = maxValue - minValue || 1
      
      // Calculate points and store for tooltip
      this.points = this.validData.map((point, index) => ({
        x: (index / (this.validData.length - 1)) * width,
        y: height - ((point.value - minValue) / range) * height,
        value: point.value,
        date: point.date
      }))
      
      // Draw simple line
      ctx.beginPath()
      ctx.strokeStyle = this.color
      ctx.lineWidth = 1
      
      ctx.moveTo(this.points[0].x, this.points[0].y)
      for (let i = 1; i < this.points.length; i++) {
        ctx.lineTo(this.points[i].x, this.points[i].y)
      }
      
      ctx.stroke()
      
      // Draw circles at data points
      ctx.fillStyle = this.color
      this.points.forEach(point => {
        ctx.beginPath()
        ctx.arc(point.x, point.y, 2, 0, 2 * Math.PI)
        ctx.fill()
      })
    },
    onMouseMove(event) {
      if (!this.points || this.points.length === 0) return
      
      const rect = this.$refs.sparklineCanvas.getBoundingClientRect()
      const mouseX = event.clientX - rect.left
      
      // Find closest point
      let closestPoint = null
      let minDistance = Infinity
      
      this.points.forEach(point => {
        const distance = Math.abs(point.x - mouseX)
        if (distance < minDistance) {
          minDistance = distance
          closestPoint = point
        }
      })
      
      if (closestPoint && minDistance < 20) { // Show tooltip within 20px
        this.tooltip.visible = true
        this.tooltip.x = closestPoint.x + 10
        this.tooltip.y = closestPoint.y - 40
        this.tooltip.value = closestPoint.value.toFixed(2)
        this.tooltip.time = this.formatTime(closestPoint.date)
      } else {
        this.tooltip.visible = false
      }
    },
    onMouseLeave() {
      this.tooltip.visible = false
    },
    formatTime(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('pl-PL', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.sparkline-container {
  width: 100%;
  margin: 0.5rem 0;
  min-height: 40px;
  position: relative;
}

canvas {
  display: block;
  width: 100%;
  max-width: 100%;
  cursor: pointer;
}

.tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  pointer-events: none;
  z-index: 10;
  white-space: nowrap;
}

.tooltip-content {
  text-align: center;
}

.tooltip-value {
  font-weight: bold;
  margin-bottom: 2px;
}

.tooltip-time {
  font-size: 10px;
  opacity: 0.8;
}
</style>
