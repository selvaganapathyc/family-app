<template>
  <div class="dashboard">
    <div class="page-header">
      <h1 class="page-title">Finance Dashboard</h1>
      <div class="month-selector">
        <select v-model="selectedMonth" class="select-input" @change="loadData">
          <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
        </select>
        <select v-model="selectedYear" class="select-input" @change="loadData">
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="summary-cards">
      <div class="summary-card summary-card--income">
        <div class="card-label">Total Income</div>
        <div class="card-amount">{{ formatCurrency(financeStore.summary.total_income) }}</div>
      </div>
      <div class="summary-card summary-card--expense">
        <div class="card-label">Total Expenses</div>
        <div class="card-amount">{{ formatCurrency(financeStore.summary.total_expenses) }}</div>
      </div>
      <div class="summary-card" :class="netBalanceClass">
        <div class="card-label">Net Balance</div>
        <div class="card-amount">{{ formatCurrency(financeStore.summary.net_balance) }}</div>
      </div>
    </div>

    <div class="dashboard-grid">
      <!-- Recent Transactions -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Recent Transactions</h2>
          <router-link to="/finance/expenses" class="section-link">View all</router-link>
        </div>
        <div v-if="financeStore.loading" class="loading-state">Loading...</div>
        <div v-else-if="recentTransactions.length === 0" class="empty-state">
          No transactions this month.
        </div>
        <div v-else class="recent-list">
          <div
            v-for="tx in recentTransactions"
            :key="tx.id"
            class="recent-item"
          >
            <div class="recent-item-left">
              <div class="recent-icon" :class="tx.type === 'income' ? 'icon--income' : 'icon--expense'">
                {{ tx.type === 'income' ? '↑' : '↓' }}
              </div>
              <div>
                <div class="recent-desc">{{ tx.description }}</div>
                <div class="recent-meta">{{ tx.category }} · {{ tx.member_name }}</div>
              </div>
            </div>
            <div class="recent-amount" :class="tx.type === 'income' ? 'amount--income' : 'amount--expense'">
              {{ tx.type === 'expense' ? '-' : '+' }}{{ formatCurrency(tx.amount) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Budget Progress -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Budget Progress</h2>
          <router-link to="/finance/budget" class="section-link">Manage</router-link>
        </div>
        <div v-if="financeStore.budgets.length === 0" class="empty-state">
          No budgets set for this month.
        </div>
        <div v-else class="budget-list">
          <div v-for="budget in financeStore.budgets" :key="budget.id" class="budget-item">
            <div class="budget-header">
              <span class="budget-category">{{ budget.category }}</span>
              <span class="budget-amounts">
                {{ formatCurrency(budget.spent || 0) }} / {{ formatCurrency(budget.amount) }}
              </span>
            </div>
            <div class="budget-bar-track">
              <div
                class="budget-bar-fill"
                :class="getBudgetBarClass(budget)"
                :style="{ width: getBudgetPercent(budget) + '%' }"
              ></div>
            </div>
            <div class="budget-remaining">
              {{ getRemainingLabel(budget) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Category Breakdown -->
    <div v-if="financeStore.summary.by_category?.length" class="dashboard-section">
      <div class="section-header">
        <h2 class="section-title">Spending by Category</h2>
      </div>
      <div class="category-grid">
        <div
          v-for="cat in financeStore.summary.by_category"
          :key="cat.category"
          class="category-card"
        >
          <div class="category-name">{{ cat.category }}</div>
          <div class="category-amount" :class="cat.type === 'income' ? 'amount--income' : 'amount--expense'">
            {{ formatCurrency(cat.total) }}
          </div>
          <div class="category-count">{{ cat.count }} transaction{{ cat.count !== 1 ? 's' : '' }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '../store/finance.store.js'

const financeStore = useFinanceStore()

const now = new Date()
const selectedMonth = ref(now.getMonth() + 1)
const selectedYear = ref(now.getFullYear())

const months = [
  { value: 1, label: 'January' },
  { value: 2, label: 'February' },
  { value: 3, label: 'March' },
  { value: 4, label: 'April' },
  { value: 5, label: 'May' },
  { value: 6, label: 'June' },
  { value: 7, label: 'July' },
  { value: 8, label: 'August' },
  { value: 9, label: 'September' },
  { value: 10, label: 'October' },
  { value: 11, label: 'November' },
  { value: 12, label: 'December' },
]

const currentYear = now.getFullYear()
const years = [currentYear - 1, currentYear, currentYear + 1]

const recentTransactions = computed(() =>
  [...financeStore.transactions]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 5),
)

const netBalanceClass = computed(() => {
  const net = financeStore.summary.net_balance
  if (net > 0) return 'summary-card--positive'
  if (net < 0) return 'summary-card--negative'
  return 'summary-card--neutral'
})

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value || 0)
}

function getBudgetPercent(budget) {
  if (!budget.amount) return 0
  return Math.min(100, ((budget.spent || 0) / budget.amount) * 100)
}

function getBudgetBarClass(budget) {
  const pct = getBudgetPercent(budget)
  if (pct >= 100) return 'bar--over'
  if (pct >= 80) return 'bar--warn'
  return 'bar--ok'
}

function getRemainingLabel(budget) {
  const remaining = budget.amount - (budget.spent || 0)
  if (remaining < 0) return `Over by ${formatCurrency(Math.abs(remaining))}`
  return `${formatCurrency(remaining)} remaining`
}

async function loadData() {
  await Promise.all([
    financeStore.fetchTransactions({ month: selectedMonth.value, year: selectedYear.value }),
    financeStore.fetchBudgets(selectedMonth.value, selectedYear.value),
    financeStore.fetchSummary(selectedMonth.value, selectedYear.value),
  ])
}

onMounted(loadData)
</script>

<style scoped>
.dashboard {
  max-width: 1100px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.month-selector {
  display: flex;
  gap: 8px;
}

.select-input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  background: white;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.summary-card {
  background: white;
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
  border-left: 4px solid #e5e7eb;
}

.summary-card--income {
  border-left-color: #10b981;
}

.summary-card--expense {
  border-left-color: #ef4444;
}

.summary-card--positive {
  border-left-color: #3b82f6;
}

.summary-card--negative {
  border-left-color: #f59e0b;
}

.summary-card--neutral {
  border-left-color: #9ca3af;
}

.card-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 8px;
}

.card-amount {
  font-size: 26px;
  font-weight: 700;
  color: #111827;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.dashboard-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.section-link {
  font-size: 13px;
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.loading-state,
.empty-state {
  color: #9ca3af;
  font-size: 14px;
  text-align: center;
  padding: 20px;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recent-item-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.recent-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.icon--income {
  background: #d1fae5;
  color: #059669;
}

.icon--expense {
  background: #fee2e2;
  color: #dc2626;
}

.recent-desc {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.recent-meta {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 2px;
}

.recent-amount {
  font-size: 15px;
  font-weight: 600;
}

.amount--income {
  color: #059669;
}

.amount--expense {
  color: #dc2626;
}

.budget-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.budget-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.budget-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.budget-category {
  font-weight: 500;
  color: #374151;
}

.budget-amounts {
  color: #6b7280;
}

.budget-bar-track {
  height: 6px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.budget-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.4s ease;
}

.bar--ok {
  background: #10b981;
}

.bar--warn {
  background: #f59e0b;
}

.bar--over {
  background: #ef4444;
}

.budget-remaining {
  font-size: 11px;
  color: #9ca3af;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.category-card {
  background: #f9fafb;
  border-radius: 10px;
  padding: 14px;
}

.category-name {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 6px;
}

.category-amount {
  font-size: 18px;
  font-weight: 700;
}

.category-count {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
}
</style>
