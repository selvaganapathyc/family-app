const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const TOKEN_KEY = 'family_app_token'
const USER_KEY = 'family_app_user'

const listeners = []

function notify(event, session) {
  listeners.forEach((cb) => cb(event, session))
}

export default {
  async signIn(email, password) {
    try {
      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      if (!res.ok) {
        const err = await res.json()
        return { data: null, error: { message: err.detail || 'Login failed' } }
      }
      const { access_token, user } = await res.json()
      localStorage.setItem(TOKEN_KEY, access_token)
      localStorage.setItem(USER_KEY, JSON.stringify(user))
      const session = { access_token, user }
      notify('SIGNED_IN', session)
      return { data: { session, user }, error: null }
    } catch (e) {
      return { data: null, error: { message: e.message } }
    }
  },

  async signOut() {
    const token = localStorage.getItem(TOKEN_KEY)
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    notify('SIGNED_OUT', null)
    try {
      await fetch(`${BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      })
    } catch {}
    return { error: null }
  },

  async getSession() {
    const token = localStorage.getItem(TOKEN_KEY)
    const userStr = localStorage.getItem(USER_KEY)
    if (!token || !userStr) return { data: { session: null }, error: null }
    const user = JSON.parse(userStr)
    return { data: { session: { access_token: token, user } }, error: null }
  },

  onAuthStateChange(callback) {
    listeners.push(callback)
    return {
      unsubscribe() {
        const i = listeners.indexOf(callback)
        if (i > -1) listeners.splice(i, 1)
      },
    }
  },

  async getAccessToken() {
    return localStorage.getItem(TOKEN_KEY)
  },
}
