import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export const MODULES = [
  { key: 'overview',   label: 'Overview',   icon: '🏠', defaultRoute: '/overview' },
  { key: 'finance',    label: 'Finance',     icon: '💰', defaultRoute: '/finance/dashboard' },
  { key: 'health',     label: 'Health',      icon: '❤️', defaultRoute: '/health/dashboard' },
  { key: 'education',  label: 'Education',   icon: '📚', defaultRoute: null, comingSoon: true },
]

export const MODULE_NAV = {
  overview: [],
  finance: [
    { path: '/finance/dashboard', label: 'Dashboard', icon: '📈' },
    { path: '/finance/expenses',  label: 'Expenses',  icon: '💸' },
    { path: '/finance/income',    label: 'Income',    icon: '💰' },
    { path: '/finance/budget',    label: 'Budget',    icon: '🎯' },
    { path: '/finance/reports',   label: 'Reports',   icon: '📋' },
  ],
  health: [
    { path: '/health/dashboard',    label: 'Dashboard',    icon: '🏥' },
    { path: '/health/vitals',       label: 'Vitals',       icon: '💓' },
    { path: '/health/medications',  label: 'Medications',  icon: '💊' },
    { path: '/health/appointments', label: 'Appointments', icon: '📅' },
  ],
  education: [],
}

export const useAppStore = defineStore('app', () => {
  const activeModule = ref('overview')

  function setActiveModule(moduleKey) {
    activeModule.value = moduleKey
  }

  // Sync activeModule from current route path
  function syncFromRoute(path) {
    const match = MODULES.find((m) => m.key !== 'overview' && path.startsWith(`/${m.key}`))
    activeModule.value = match ? match.key : 'overview'
  }

  return { activeModule, setActiveModule, syncFromRoute }
})
