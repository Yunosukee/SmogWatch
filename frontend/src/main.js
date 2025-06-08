import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import StationsList from './components/StationsList.vue'
import StationDetails from './components/StationDetails.vue'

const routes = [
  { path: '/', component: StationsList },
  { path: '/station/:id', component: StationDetails, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')