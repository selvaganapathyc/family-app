const DashboardView = () => import('../views/DashboardView.vue')
const VitalsView = () => import('../views/VitalsView.vue')
const MedicationsView = () => import('../views/MedicationsView.vue')
const AppointmentsView = () => import('../views/AppointmentsView.vue')

const healthRoutes = [
  { path: '/health', redirect: '/health/dashboard' },
  {
    path: '/health/dashboard',
    name: 'HealthDashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/health/vitals',
    name: 'HealthVitals',
    component: VitalsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/health/medications',
    name: 'HealthMedications',
    component: MedicationsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/health/appointments',
    name: 'HealthAppointments',
    component: AppointmentsView,
    meta: { requiresAuth: true },
  },
]

export default healthRoutes
