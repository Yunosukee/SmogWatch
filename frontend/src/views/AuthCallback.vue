<template>
  <CardCenter>
    <div class="callback-container">
      <div v-if="loading">
        <LoadingSpinner />
        <h2>Przetwarzanie logowania...</h2>
        <p>Proszę czekać...</p>
      </div>

      <div v-if="error">
        <div>❌</div>
        <h2>Błąd logowania</h2>
        <p>{{ error }}</p>
        <button @click="goToLogin">Spróbuj ponownie</button>
      </div>

      <div v-if="success">
        <div>✅</div>
        <h2>Logowanie udane!</h2>
        <p>Przekierowywanie...</p>
      </div>
    </div>
  </CardCenter>
</template>

<script>
import CardCenter from '@/components/CardCenter.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { useAuthStore } from '@/stores/auth'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'AuthCallback',
  components: {
    CardCenter,
    LoadingSpinner
  },
  setup() {
    const loading = ref(true)
    const error = ref('')
    const success = ref(false)
    const authStore = useAuthStore()
    const router = useRouter()

    const goToLogin = () => {
      router.push('/login')
    }

    onMounted(async () => {
      try {
        // Handle OAuth callback
        const urlParams = new URLSearchParams(window.location.search)
        const code = urlParams.get('code')
        const state = urlParams.get('state')

        if (!code) {
          throw new Error('Brak kodu autoryzacji')
        }

        await authStore.handleCallback(code, state)
        success.value = true
        loading.value = false

        // Check for redirect parameter and redirect to intended destination
        const redirectUrl = sessionStorage.getItem('auth_redirect') || '/'
        sessionStorage.removeItem('auth_redirect') // Clean up
        
        // Redirect to intended destination or home after successful login
        setTimeout(() => {
          router.push(redirectUrl)
        }, 2000)

      } catch (err) {
        error.value = err.message || 'Wystąpił błąd podczas logowania'
        loading.value = false
        console.error('Auth callback error:', err)
      }
    })

    return {
      loading,
      error,
      success,
      goToLogin
    }
  }
}
</script>

<style scoped>
.callback-container {
  text-align: center;
  padding: 2rem;
}

.callback-container h2 {
  margin: 1rem 0;
  color: #334155;
}

.callback-container p {
  color: #64748b;
  margin-bottom: 1rem;
}

.callback-container button {
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.callback-container button:hover {
  background-color: #2563eb;
}
</style>
