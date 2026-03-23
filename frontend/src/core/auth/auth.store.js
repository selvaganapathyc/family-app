import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { signIn, signOut, getSession, onAuthStateChange } from './index.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const session = ref(null)
  const loading = ref(false)
  const initialized = ref(false)

  const isAuthenticated = computed(() => !!session.value && !!user.value)

  /**
   * Initialize auth state from existing session and subscribe to changes.
   */
  async function initAuth() {
    if (initialized.value) return

    loading.value = true
    try {
      const { data, error } = await getSession()
      if (error) throw error

      session.value = data.session
      user.value = data.session?.user ?? null

      // Listen for auth changes (login, logout, token refresh)
      onAuthStateChange((event, newSession) => {
        session.value = newSession
        user.value = newSession?.user ?? null
      })
    } catch (err) {
      console.error('Failed to initialize auth:', err.message)
      session.value = null
      user.value = null
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  /**
   * Log in with email and password.
   * Returns { error } — error is null on success.
   */
  async function login(email, password) {
    loading.value = true
    try {
      const { data, error } = await signIn(email, password)
      if (error) return { error }

      session.value = data.session
      user.value = data.user
      return { error: null }
    } catch (err) {
      return { error: err }
    } finally {
      loading.value = false
    }
  }

  /**
   * Log out the current user.
   */
  async function logout() {
    loading.value = true
    try {
      await signOut()
      session.value = null
      user.value = null
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    session,
    loading,
    initialized,
    isAuthenticated,
    initAuth,
    login,
    logout,
  }
})
