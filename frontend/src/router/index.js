import { createRouter, createWebHistory } from 'vue-router'
import authRoutes from '@/core/auth/auth.routes.js'
import overviewRoutes from '@/modules/overview/router/overview.routes.js'
import financeRoutes from '@/modules/finance/router/finance.routes.js'
import healthRoutes from '@/modules/health/router/health.routes.js'
import { useAuthStore } from '@/core/auth/auth.store.js'

const routes = [
  { path: '/', redirect: '/overview' },
  ...authRoutes,
  ...overviewRoutes,
  ...financeRoutes,
  ...healthRoutes,
  { path: '/:pathMatch(.*)*', redirect: '/overview' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (!authStore.initialized) {
    await authStore.initAuth()
  }

  const requiresAuth = to.meta.requiresAuth !== false

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/overview')
  } else {
    next()
  }
})

export default router
