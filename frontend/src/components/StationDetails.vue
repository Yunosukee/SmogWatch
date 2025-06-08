<template>
  <div class="station-details">
    <button @click="goBack" class="back-button">
      ← Powrót do listy stacji
    </button>
    
    <div v-if="loading" class="loading">
      Ładowanie danych stacji...
    </div>
    
    <div v-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-if="!loading && !error" class="station-info">
      <div class="station-header">
        <h2>{{ stationInfo.stationName }}</h2>
        <p class="location">📍 {{ stationInfo.city?.name }}, {{ stationInfo.addressStreet }}</p>
      </div>
      
      <div v-if="airQualityIndex" class="air-quality-card">
        <h3>Indeks Jakości Powietrza</h3>
        <div class="quality-index" :class="getQualityClass(airQualityIndex.stIndexLevel)">
          <div class="index-value">
            {{ airQualityIndex.stIndexLevel?.indexLevelName || 'Brak danych' }}
          </div>
          <div class="index-date" v-if="airQualityIndex.stCalcDate">
            Obliczono: {{ formatDate(airQualityIndex.stCalcDate) }}
          </div>
        </div>
      </div>
      
      <div class="sensors-section">
        <h3>Dane z sensorów</h3>
        <div class="sensors-grid">
          <div 
            v-for="sensor in sensorsWithData" 
            :key="sensor.id"
            class="sensor-card"
          >
            <h4>{{ sensor.param.paramName }}</h4>
            <p class="param-code">{{ sensor.param.paramCode }}</p>
            
            <div v-if="sensor.data && sensor.data.values && sensor.data.values.length > 0" class="sensor-data">
              <div class="current-value">
                <span class="value">{{ getCurrentValue(sensor.data.values) }}</span>
                <span class="unit">µg/m³</span>
              </div>
              <div class="last-update">
                Ostatni pomiar: {{ formatDate(getLastMeasurementDate(sensor.data.values)) }}
              </div>
            </div>
            
            <div v-else class="no-data">
              Brak dostępnych danych
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StationDetails',
  props: ['id'],
  data() {
    return {
      stationInfo: {},
      sensors: [],
      sensorsWithData: [],
      airQualityIndex: null,
      loading: true,
      error: null
    }
  },
  async mounted() {
    await this.fetchStationData()
  },
  methods: {
    async fetchStationData() {
      try {
        this.loading = true
        
        const stationsResponse = await axios.get('http://localhost:5000/api/stations')
        this.stationInfo = stationsResponse.data.find(station => station.id == this.id) || {}
        
        const sensorsResponse = await axios.get(`http://localhost:5000/api/station/${this.id}/sensors`)
        this.sensors = sensorsResponse.data
        
        const airQualityResponse = await axios.get(`http://localhost:5000/api/station/${this.id}/air-quality`)
        this.airQualityIndex = airQualityResponse.data
        
        await this.fetchSensorsData()
        
      } catch (error) {
        this.error = 'Nie udało się pobrać danych stacji'
        console.error('Error fetching station data:', error)
      } finally {
        this.loading = false
      }
    },
    
    async fetchSensorsData() {
      const sensorsWithData = []
      
      for (const sensor of this.sensors) {
        try {
          const dataResponse = await axios.get(`http://localhost:5000/api/sensor/${sensor.id}/data`)
          sensorsWithData.push({
            ...sensor,
            data: dataResponse.data
          })
        } catch (error) {
          console.error(`Error fetching data for sensor ${sensor.id}:`, error)
          sensorsWithData.push({
            ...sensor,
            data: null
          })
        }
      }
      
      this.sensorsWithData = sensorsWithData
    },
    
    getCurrentValue(values) {
      const validValues = values.filter(v => v.value !== null)
      return validValues.length > 0 ? validValues[0].value : 'Brak danych'
    },
    
    getLastMeasurementDate(values) {
      const validValues = values.filter(v => v.value !== null)
      return validValues.length > 0 ? validValues[0].date : null
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Brak danych'
      const date = new Date(dateString)
      return date.toLocaleString('pl-PL')
    },
    
    getQualityClass(indexLevel) {
      if (!indexLevel) return 'unknown'
      
      const levelName = indexLevel.indexLevelName?.toLowerCase()
      if (levelName?.includes('bardzo dobry')) return 'very-good'
      if (levelName?.includes('dobry')) return 'good'
      if (levelName?.includes('umiarkowany')) return 'moderate'
      if (levelName?.includes('dostateczny')) return 'sufficient'
      if (levelName?.includes('zły')) return 'bad'
      if (levelName?.includes('bardzo zły')) return 'very-bad'
      return 'unknown'
    },
    
    goBack() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.back-button {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  margin-bottom: 2rem;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #5a6fd8;
}

.station-header {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.station-header h2 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.location {
  color: #666;
  font-size: 1.1rem;
}

.air-quality-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.air-quality-card h3 {
  color: #333;
  margin-bottom: 1rem;
}

.quality-index {
  text-align: center;
  padding: 1.5rem;
  border-radius: 8px;
  color: white;
  font-weight: bold;
}

.very-good { background-color: #4CAF50; }
.good { background-color: #8BC34A; }
.moderate { background-color: #FFC107; color: #333; }
.sufficient { background-color: #FF9800; }
.bad { background-color: #F44336; }
.very-bad { background-color: #9C27B0; }
.unknown { background-color: #9E9E9E; }

.index-value {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.index-date {
  font-size: 0.9rem;
  opacity: 0.9;
}

.sensors-section h3 {
  color: #333;
  margin-bottom: 1.5rem;
}

.sensors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.sensor-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.sensor-card h4 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.param-code {
  color: #667eea;
  font-weight: 600;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.current-value {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.value {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.unit {
  color: #666;
  font-size: 1rem;
}

.last-update {
  color: #666;
  font-size: 0.9rem;
}

.no-data {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}
</style>