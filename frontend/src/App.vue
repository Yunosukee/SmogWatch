<template>
  <div id="app">
    <header class="header">
      <div class="header-content">
        <div class="header-left">
          <h1>🌬️ SmogWatch</h1>
          <p>Monitor jakości powietrza w Polsce</p>
          <!-- UserProfile will appear here on mobile -->
          <div class="mobile-user-profile">
            <UserProfile />
          </div>
        </div>
        <div class="header-right">
          <!-- UserProfile appears here on desktop -->
          <div class="desktop-user-profile">
            <UserProfile />
          </div>
        </div>
      </div>
    </header>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import UserProfile from './components/user/UserProfile.vue'
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  components: {
    UserProfile
  },
  setup() {
    const authStore = useAuthStore()

    // Check authentication status on app load
    onMounted(async () => {
      try {
        await authStore.checkAuth()
      } catch (error) {
        console.error('Failed to check auth status:', error)
      }
    })

    return {
      authStore
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  text-align: left;
}

.header-right {
  min-width: 200px;
}

/* Desktop: show user profile in header-right, hide in header-left */
.desktop-user-profile {
  display: block;
}

.mobile-user-profile {
  display: none;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .header {
    padding: 1.5rem 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .header-left {
    text-align: center;
  }
  
  .header-right {
    min-width: unset;
  }
  
  /* Mobile: hide user profile in header-right, show in header-left */
  .desktop-user-profile {
    display: none;
  }
  
  .mobile-user-profile {
    display: block;
    margin-top: 1rem;
  }
  
  .header h1 {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 1rem;
  }
  
  .header h1 {
    font-size: 1.75rem;
  }
}

.main-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.error {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  text-align: center;
}
</style>