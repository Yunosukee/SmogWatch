<template>
  <div class="user-profile">
    <div v-if="authStore.isAuthenticated" class="user-info">
      <div class="user-avatar">
        <span class="avatar-text">{{ userInitials }}</span>
      </div>
      <div class="user-details">
        <h3 class="user-name">{{ authStore.userInfo?.name || 'Użytkownik' }}</h3>
        <p class="user-email">{{ authStore.userInfo?.email }}</p>
      </div>
      <button 
        @click="logout" 
        :disabled="authStore.isLoading"
        class="logout-button"
      >
        <span v-if="authStore.isLoading">Wylogowywanie...</span>
        <span v-else>Wyloguj</span>
      </button>
    </div>
    
    <div v-else class="login-prompt">
      <button @click="goToLogin" class="login-button">
        Zaloguj się
      </button>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'UserProfile',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const userInitials = computed(() => {
      const name = authStore.userInfo?.name
      if (!name) return 'U'
      
      const parts = name.split(' ')
      if (parts.length >= 2) {
        return parts[0][0].toUpperCase() + parts[1][0].toUpperCase()
      }
      return name[0].toUpperCase()
    })

    const logout = async () => {
      try {
        await authStore.logout()
      } catch (error) {
        console.error('Logout failed:', error)
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      authStore,
      userInitials,
      logout,
      goToLogin
    }
  }
}
</script>

<style scoped>
.user-profile {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  min-width: 0; /* Prevent flex shrinking issues */
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0; /* Prevent avatar from shrinking */
}

.user-details {
  flex: 1;
  min-width: 0; /* Allow text to truncate properly */
}

.user-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  margin: 0;
  font-size: 0.875rem;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.logout-button {
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
  white-space: nowrap;
  flex-shrink: 0;
}

.logout-button:hover:not(:disabled) {
  background-color: #c82333;
}

.logout-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-prompt {
  text-align: center;
}

.login-button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
  white-space: nowrap;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .user-profile {
    padding: 0.75rem;
  }
  
  .user-info {
    gap: 0.75rem;
  }
  
  .user-avatar {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .user-name {
    font-size: 0.9rem;
  }
  
  .user-email {
    font-size: 0.8rem;
  }
  
  .logout-button {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
  
  .login-button {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
}

/* Extra small screens */
@media (max-width: 480px) {
  .user-info {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
  
  .user-details {
    order: 2;
    width: 100%;
  }
  
  .user-avatar {
    order: 1;
    margin: 0 auto;
  }
  
  .logout-button {
    order: 3;
    width: 100%;
  }
  
  .user-name,
  .user-email {
    white-space: normal;
    text-align: center;
  }
  
  .login-button {
    width: 100%;
  }
}

/* Very small screens */
@media (max-width: 320px) {
  .user-profile {
    padding: 0.5rem;
  }
  
  .user-avatar {
    width: 36px;
    height: 36px;
    font-size: 0.9rem;
  }
  
  .user-name {
    font-size: 0.85rem;
  }
  
  .user-email {
    font-size: 0.75rem;
  }
  
  .logout-button,
  .login-button {
    font-size: 0.8rem;
    padding: 0.5rem;
  }
}
</style>
