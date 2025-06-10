<template>
  <div class="historical-chart">
    <div class="chart-header">
      <h4>{{ sensorName }} - Dane historyczne</h4>
      <div class="controls">
        <select v-model="selectedPeriod" class="period-selector" :disabled="loading">
          <option value="3">Ostatnie 3 dni</option>
          <option value="7">Ostatni tydzień</option>
          <option value="14">Ostatnie 2 tygodnie</option>
          <option value="30">Ostatni miesiąc</option>
        </select>
        <button 
          @click="fetchHistoricalData" 
          :disabled="loading" 
          class="load-data-button"
        >
          {{ loading ? 'Ładowanie...' : 'Pokaż wykres' }}
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      Ładowanie danych historycznych...
    </div>
    
    <div v-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-if="!loading && !error && chartData" class="chart-container">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    
    <div v-if="!loading && !error && !chartData && !hasLoadedOnce" class="no-data">
      Kliknij "Pokaż wykres" aby załadować dane historyczne
    </div>
    
    <div v-if="!loading && !error && !chartData && hasLoadedOnce" class="no-data">
      Brak danych historycznych dla tego sensora
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    LineElement,
    PointElement,
    TimeScale,
    Title,
    Tooltip
} from 'chart.js'
import 'chartjs-adapter-date-fns'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
)

export default {
  name: 'HistoricalChart',
  components: {
    Line
  },
  props: {
    sensorId: {
      type: Number,
      required: true
    },
    sensorName: {
      type: String,
      required: true
    },
    paramCode: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      selectedPeriod: '7',
      historicalData: null,
      chartData: null,
      loading: false,
      error: null,
      hasLoadedOnce: false
    }
  },
  computed: {
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `${this.paramCode} - ${this.selectedPeriod} dni`,
            font: {
              size: 16
            }
          },
          legend: {
            display: false
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              label: (context) => {
                return `${context.parsed.y} µg/m³`
              }
            }
          }
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'hour',
              displayFormats: {
                hour: 'dd.MM HH:mm'
              },
              tooltipFormat: 'dd.MM.yyyy HH:mm'
            },
            title: {
              display: true,
              text: 'Data i godzina'
            }
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Stężenie (µg/m³)'
            }
          }
        },
        interaction: {
          mode: 'nearest',
          axis: 'x',
          intersect: false
        }
      }
    }
  },
  // Remove automatic loading - data will be loaded on demand
  methods: {
    async fetchHistoricalData() {
      try {
        this.loading = true
        this.error = null
        this.hasLoadedOnce = true
        
        const response = await axios.get(
          `http://localhost:5000/api/sensor/${this.sensorId}/historical?days=${this.selectedPeriod}`
        )
        
        this.historicalData = response.data
        this.processChartData()
        
      } catch (error) {
        this.error = 'Nie udało się pobrać danych historycznych'
        console.error('Error fetching historical data:', error)
      } finally {
        this.loading = false
      }
    },
    
    processChartData() {
      if (!this.historicalData || !this.historicalData['Lista archiwalnych wyników pomiarów']) {
        this.chartData = null
        return
      }
      
      const measurements = this.historicalData['Lista archiwalnych wyników pomiarów']
      
      // Filter and sort valid measurements
      const validData = measurements
        .filter(item => item.Wartość !== null && item.Data)
        .sort((a, b) => new Date(a.Data) - new Date(b.Data))
      
      if (validData.length === 0) {
        this.chartData = null
        return
      }
      
      // Prepare data for Chart.js
      const labels = validData.map(item => new Date(item.Data))
      const values = validData.map(item => item.Wartość)
      
      this.chartData = {
        labels: labels,
        datasets: [{
          label: this.paramCode,
          data: values,
          borderColor: this.getLineColor(),
          backgroundColor: this.getLineColor() + '20',
          borderWidth: 2,
          pointRadius: 2,
          pointHoverRadius: 4,
          fill: true,
          tension: 0.1
        }]
      }
    },
    
    getLineColor() {
      // Different colors for different pollutants
      const colors = {
        'PM10': '#FF6B6B',
        'PM2.5': '#4ECDC4',
        'NO2': '#45B7D1',
        'SO2': '#96CEB4',
        'O3': '#FFEAA7',
        'CO': '#DDA0DD'
      }
      return colors[this.paramCode] || '#667eea'
    }
  }
}
</script>

<style scoped>
.historical-chart {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-header h4 {
  color: #333;
  margin: 0;
  font-size: 1.2rem;
}

.controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.period-selector {
  padding: 0.5rem 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  background-color: white;
  color: #333;
  font-size: 0.9rem;
  cursor: pointer;
  transition: border-color 0.3s;
}

.period-selector:focus {
  outline: none;
  border-color: #667eea;
}

.period-selector:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.load-data-button {
  padding: 0.5rem 1rem;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
}

.load-data-button:hover:not(:disabled) {
  background-color: #5a6fd8;
}

.load-data-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.chart-container {
  height: 400px;
  position: relative;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  text-align: center;
  padding: 2rem;
  color: #e74c3c;
  background-color: #fdf2f2;
  border-radius: 8px;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #999;
  font-style: italic;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .controls {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .period-selector,
  .load-data-button {
    width: 100%;
  }
  
  .chart-container {
    height: 300px;
  }
}
</style>
