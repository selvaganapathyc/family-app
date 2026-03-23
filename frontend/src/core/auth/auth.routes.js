import LoginView from './LoginView.vue'

const authRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: {
      requiresAuth: false,
    },
  },
]

export default authRoutes
