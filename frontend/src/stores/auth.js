import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!user.value)

  async function login(email, password) {
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/token/', { email, password })
      const { access, refresh } = response.data

      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)

      await fetchProfile()
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null

    try {
      await api.post('/users/register/', userData)
      return true
    } catch (err) {
      error.value = err.response?.data || 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchProfile() {
    try {
      const response = await api.get('/users/profile/')
      user.value = response.data
    } catch (err) {
      console.error('Failed to fetch profile:', err)
    }
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    fetchProfile,
    logout,
  }
})