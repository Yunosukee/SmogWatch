<template>
  <CardCenter>
    <div class="login-container">
      <div class="login-header">
        <h2>Witaj! 🌬️</h2>
        <p>Zaloguj się do SmogWatch</p>
      </div>

      <div class="login-form">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="success" class="success-message">
          {{ success }}
        </div>

        <div class="button-group">
          <button
            type="button"
            @click="onAuthentikLogin"
            :disabled="authStore.isLoading"
            class="login-btn primary"
          >
            {{ authStore.isLoading ? 'Przekierowywanie...' : 'Zaloguj przez Authentik' }}
          </button>
        </div>
      </div>
    </div>
  </CardCenter>
</template>

<script>
import CardCenter from '@/components/CardCenter.vue'
import { useAuthStore } from '@/stores/auth'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'LoginView',
  components: {
    CardCenter
  },
  setup() {
    const error = ref('')
    const success = ref('')
    const authStore = useAuthStore()
    const route = useRoute()
    const router = useRouter()

    onMounted(() => {
      // Store redirect URL if provided
      const redirectUrl = route.query.redirect
      if (redirectUrl) {
        sessionStorage.setItem('auth_redirect', redirectUrl)
      }
      
      // If user is already authenticated, redirect them
      if (authStore.isAuthenticated) {
        const redirectPath = redirectUrl || '/'
        router.push(redirectPath)
      }
    })

    const onAuthentikLogin = async () => {
      error.value = ''
      success.value = ''
      try {
        await authStore.login()
      } catch (err) {
        error.value = 'Błąd podczas logowania'
        console.error('Login failed:', err)
      }
    }

    return {
      error,
      success,
      authStore,
      onAuthentikLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  width: 100%;
  text-align: center;
}

.login-header {
  margin-bottom: 2rem;
}

.login-header h2 {
  margin-bottom: 0.5rem;
  font-size: 1.875rem;
  font-weight: 700;
  color: #334155;
}

.login-header p {
  font-size: 0.875rem;
  color: #64748b;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.error-message {
  padding: 0.75rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  color: #dc2626;
  font-size: 0.875rem;
  font-weight: 500;
}

.success-message {
  padding: 0.75rem;
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 0.5rem;
  color: #16a34a;
  font-size: 0.875rem;
  font-weight: 500;
}

.button-group {
  display: flex;
  justify-content: center;
}

.login-btn {
  font-weight: 600;
  padding: 0.75rem 2rem;
  border-radius: 0.75rem;
  transition: all 0.2s;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border: none;
  cursor: pointer;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
</style>
