import { UserManager } from 'oidc-client-ts'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { oidcConfig } from '../config/oauth.js'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  // OIDC UserManager instance
  const userManager = new UserManager(oidcConfig)

  // Event handlers
  // Setup event handlers for automatic token renewal
  userManager.events.addUserLoaded((loadedUser) => {
    console.log('✅ User loaded!')
    // Update user state when token is refreshed
    user.value = loadedUser
  })

  userManager.events.addUserUnloaded(() => {
    console.log('🧹 User unloaded, clearing user state...')
    user.value = null
  })

  userManager.events.addSilentRenewError((renewError) => {
    console.error('❌ Silent renewal error:', renewError)
    error.value = 'Token renewal failed'
  })

  userManager.events.addUserSignedOut(() => {
    console.log('🚶 User signed out, cleaning user state...')
    user.value = null
  })

  userManager.events.addAccessTokenExpired(() => {
    console.log('⌛ Token expired, clearing user state...')
    user.value = null
  })

  userManager.events.addUserSessionChanged(() => {
    console.log('👀 User session change detected')

    // Check current session state
    userManager.getUser().then((currentUser) => {
      if (!currentUser || currentUser.expired) {
        console.log('🔐 User session has expired or was closed on the server')
        user.value = null
      } else {
        console.log('✓ User session is still active')
      }
    })
  })

  // Getters
  const isAuthenticated = computed(() => !!user.value && !user.value.expired)
  const userInfo = computed(() => {
    if (!user.value?.profile) return null
    const { name, email, sub: id } = user.value.profile
    return { name, email, id }
  })

  // Actions
  const login = async () => {
    isLoading.value = true
    error.value = null
    try {
      await userManager.signinRedirect()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const handleCallback = async () => {
    isLoading.value = true
    error.value = null
    try {
      const callbackUser = await userManager.signinRedirectCallback()
      user.value = callbackUser
      return callbackUser
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Callback handling failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    isLoading.value = true
    error.value = null
    try {
      await userManager.signoutRedirect()
      user.value = null // Clear user after successful signout
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Logout failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const checkAuth = async () => {
    isLoading.value = true
    error.value = null
    try {
      const currentUser = await userManager.getUser()
      user.value = currentUser
      return !!currentUser && !currentUser.expired
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Auth check failed'
      user.value = null
      return false
    } finally {
      isLoading.value = false
    }
  }

  const refreshToken = async () => {
    isLoading.value = true
    error.value = null
    try {
      console.log('🔃 Silently refreshing token...')
      const refreshedUser = await userManager.signinSilent()
      console.log('✅ Token refreshed successfully!')
      user.value = refreshedUser
      return true
    } catch (err) {
      console.error('❌ Token refresh failed:', err)
      const errorMessage = err instanceof Error ? err.message : String(err)

      // Check for a specific type of error
      if (errorMessage.includes('requires End-User authentication')) {
        // This error indicates that the session has expired and the user needs to log in again
        error.value = 'Session expired. Re-login required.'
        user.value = null // In this case, the user needs to log in again
      } else if (errorMessage.includes('No state in response')) {
        // Common error when there is no session
        error.value = 'No active authentication session.'
        user.value = null
      } else {
        // Other errors - may be temporary
        error.value = `Token refresh failed: ${errorMessage}`
      }
      return false
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    userInfo,
    login,
    handleCallback,
    logout,
    checkAuth,
    refreshToken,
  }
})
