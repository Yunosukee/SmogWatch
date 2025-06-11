import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import StationDetails from './components/StationDetails.vue'
import StationsList from './components/StationsList.vue'
import AuthCallback from './views/AuthCallback.vue'
import LoginView from './views/LoginView.vue'

const routes = [
  { path: '/', component: StationsList },
  { path: '/station/:id', component: StationDetails, props: true },
  { path: '/login', component: LoginView },
  { path: '/auth/callback', component: AuthCallback }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)

// Route guard for authentication
import { useAuthStore } from './stores/auth'

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Public routes that don't require authentication
  const publicRoutes = ['/login', '/auth/callback']
  const isPublicRoute = publicRoutes.includes(to.path)
  
  // If going to a public route, allow access
  if (isPublicRoute) {
    next()
    return
  }
  
  // Check authentication status
  try {
    // Check if user is already authenticated
    if (!authStore.isAuthenticated) {
      // Try to check auth status (e.g., from stored tokens)
      await authStore.checkAuth()
    }
    
    // If still not authenticated, redirect to login
    if (!authStore.isAuthenticated) {
      console.log('🔐 User not authenticated, redirecting to login...')
      // Store the intended destination for redirect after login
      const redirectPath = to.fullPath !== '/login' ? to.fullPath : '/'
      next(`/login?redirect=${encodeURIComponent(redirectPath)}`)
    } else {
      // User is authenticated, allow access
      next()
    }
  } catch (error) {
    console.error('❌ Auth check failed:', error)
    // On auth check failure, redirect to login
    const redirectPath = to.fullPath !== '/login' ? to.fullPath : '/'
    next(`/login?redirect=${encodeURIComponent(redirectPath)}`)
  }
})

app.mount('#app')