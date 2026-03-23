import DashboardView from '../views/DashboardView.vue'
import ExpensesView from '../views/ExpensesView.vue'
import IncomeView from '../views/IncomeView.vue'
import BudgetView from '../views/BudgetView.vue'
import ReportsView from '../views/ReportsView.vue'

const financeRoutes = [
  {
    path: '/finance',
    redirect: '/finance/dashboard',
  },
  {
    path: '/finance/dashboard',
    name: 'FinanceDashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/finance/expenses',
    name: 'FinanceExpenses',
    component: ExpensesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/finance/income',
    name: 'FinanceIncome',
    component: IncomeView,
    meta: { requiresAuth: true },
  },
  {
    path: '/finance/budget',
    name: 'FinanceBudget',
    component: BudgetView,
    meta: { requiresAuth: true },
  },
  {
    path: '/finance/reports',
    name: 'FinanceReports',
    component: ReportsView,
    meta: { requiresAuth: true },
  },
]

export default financeRoutes
