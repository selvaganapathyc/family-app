import OverviewView from '../views/OverviewView.vue'

const overviewRoutes = [
  {
    path: '/overview',
    name: 'Overview',
    component: OverviewView,
    meta: { requiresAuth: true },
  },
]

export default overviewRoutes
