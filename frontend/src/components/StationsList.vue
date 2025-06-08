<template>
  <div class="stations-list">
    <h2>Stacje Pomiarowe</h2>
    
    <div v-if="loading" class="loading">
      Ładowanie stacji...
    </div>
    
    <div v-if="error" class="error">
      {{ error }}
    </div>
    
    <div class="search-box">
      <input 
        v-model="searchTerm" 
        type="text" 
        placeholder="Szukaj stacji po nazwie miasta..."
        class="search-input"
      >
    </div>
    
    <div class="stations-grid" v-if="!loading && !error">
      <div 
        v-for="station in filteredStations" 
        :key="station.id"
        class="station-card"
        @click="goToStation(station.id)"
      >
        <h3>{{ station.stationName }}</h3>
        <p class="city">📍 {{ station.city.name }}</p>
        <p class="address">{{ station.addressStreet }}</p>
        <div class="station-meta">
          <span class="province">{{ station.city.commune.provinceName }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StationsList',
  data() {
    return {
      stations: [],
      loading: true,
      error: null,
      searchTerm: ''
    }
  },
  computed: {
    filteredStations() {
      if (!this.searchTerm) return this.stations
      
      return this.stations.filter(station => 
        station.city.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        station.stationName.toLowerCase().includes(this.searchTerm.toLowerCase())
      )
    }
  },
  async mounted() {
    await this.fetchStations()
  },
  methods: {
    async fetchStations() {
      try {
        this.loading = true
        const response = await axios.get('http://localhost:5000/api/stations')
        this.stations = response.data
      } catch (error) {
        this.error = 'Nie udało się pobrać listy stacji'
        console.error('Error fetching stations:', error)
      } finally {
        this.loading = false
      }
    },
    goToStation(stationId) {
      this.$router.push(`/station/${stationId}`)
    }
  }
}
</script>

<style scoped>
.stations-list h2 {
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.search-box {
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #667eea;
}

.stations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.station-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #eee;
}

.station-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #667eea;
}

.station-card h3 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.city {
  color: #667eea;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.address {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.station-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.province {
  background-color: #f0f2f5;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: #555;
}
</style>