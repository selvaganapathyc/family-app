<template>
  <div class="reports-view">
    <div class="page-header">
      <h1 class="page-title">Monthly Report</h1>
      <div class="month-selector">
        <select v-model="selectedMonth" class="select-input" @change="loadReport">
          <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
        </select>
        <select v-model="selectedYear" class="select-input" @change="loadReport">
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
      </div>
    </div>

    <div v-if="financeStore.loading" class="loading-state">Loading report...</div>
    <template v-else>
      <!-- Summary Cards -->
      <div class="summary-cards">
        <div class="summary-card summary-card--income">
          <div class="card-icon">↑</div>
          <div>
            <div class="card-label">Total Income</div>
            <div class="card-amount">{{ formatCurrency(financeStore.summary.total_income) }}</div>
          </div>
        </div>
        <div class="summary-card summary-card--expense">
          <div class="card-icon">↓</div>
          <div>
            <div class="card-label">Total Expenses</div>
            <div class="card-amount">{{ formatCurrency(financeStore.summary.total_expenses) }}</div>
          </div>
        </div>
        <div class="summary-card" :class="netClass">
          <div class="card-icon">≡</div>
          <div>
            <div class="card-label">Net Balance</div>
            <div class="card-amount">{{ formatCurrency(financeStore.summary.net_balance) }}</div>
          </div>
        </div>
      </div>

      <!-- Income vs Expense Bar -->
      <div class="report-section">
        <h2 class="section-title">Income vs Expenses</h2>
        <div class="comparison-bar-wrapper">
          <div class="comparison-label">
            <span class="income-label">Income {{ formatCurrency(financeStore.summary.total_income) }}</span>
            <span class="expense-label">Expenses {{ formatCurrency(financeStore.summary.total_expenses) }}</span>
          </div>
          <div class="comparison-bar-track">
            <div class="comparison-bar-income" :style="{ width: incomeWidth + '%' }"></div>
            <div class="comparison-bar-expense" :style="{ width: expenseWidth + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- Category Breakdown -->
      <div class="report-grid">
        <!-- Expense by Category -->
        <div class="report-section">
          <h2 class="section-title">Expenses by Category</h2>
          <div v-if="expenseCategories.length === 0" class="empty-state">No expenses.</div>
          <div v-else class="category-rows">
            <div
              v-for="cat in expenseCategories"
              :key="cat.category"
              class="category-row"
            >
              <div class="cat-info">
                <span class="cat-name">{{ cat.category }}</span>
                <span class="cat-count">{{ cat.count }} txn</span>
              </div>
              <div class="cat-bar-track">
                <div
                  class="cat-bar-fill cat-bar-fill--expense"
                  :style="{ width: getCatPercent(cat, 'expense') + '%' }"
                ></div>
              </div>
              <div class="cat-amount amount--expense">
                {{ formatCurrency(cat.total) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Income by Category -->
        <div class="report-section">
          <h2 class="section-title">Income by Category</h2>
          <div v-if="incomeCategories.length === 0" class="empty-state">No income.</div>
          <div v-else class="category-rows">
            <div
              v-for="cat in incomeCategories"
              :key="cat.category"
              class="category-row"
            >
              <div class="cat-info">
                <span class="cat-name">{{ cat.category }}</span>
                <span class="cat-count">{{ cat.count }} txn</span>
              </div>
              <div class="cat-bar-track">
                <div
                  class="cat-bar-fill cat-bar-fill--income"
                  :style="{ width: getCatPercent(cat, 'income') + '%' }"
                ></div>
              </div>
              <div class="cat-amount amount--income">
                {{ formatCurrency(cat.total) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Spending by Member -->
      <div class="report-section">
        <h2 class="section-title">Transactions by Member</h2>
        <div class="member-table-wrapper">
          <table class="member-table">
            <thead>
              <tr>
                <th>Member</th>
                <th class="text-right">Income</th>
                <th class="text-right">Expenses</th>
                <th class="text-right">Net</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="member in memberSummary" :key="member.name">
                <td>
                  <span class="member-badge">{{ member.name }}</span>
                </td>
                <td class="text-right amount--income">{{ formatCurrency(member.income) }}</td>
                <td class="text-right amount--expense">{{ formatCurrency(member.expense) }}</td>
                <td class="text-right" :class="member.net >= 0 ? 'amount--income' : 'amount--expense'">
                  {{ formatCurrency(member.net) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '../store/finance.store.js'
import { FAMILY_MEMBERS } from '../index.js'

const financeStore = useFinanceStore()

const now = new Date()
const selectedMonth = ref(now.getMonth() + 1)
const selectedYear = ref(now.getFullYear())

const months = [
  { value: 1, label: 'January' }, { value: 2, label: 'February' },
  { value: 3, label: 'March' }, { value: 4, label: 'April' },
  { value: 5, label: 'May' }, { value: 6, label: 'June' },
  { value: 7, label: 'July' }, { value: 8, label: 'August' },
  { value: 9, label: 'September' }, { value: 10, label: 'October' },
  { value: 11, label: 'November' }, { value: 12, label: 'December' },
]
const currentYear = now.getFullYear()
const years = [currentYear - 1, currentYear, currentYear + 1]

const expenseCategories = computed(() =>
  (financeStore.summary.by_category || [])
    .filter((c) => c.type === 'expense')
    .sort((a, b) => b.total - a.total),
)

const incomeCategories = computed(() =>
  (financeStore.summary.by_category || [])
    .filter((c) => c.type === 'income')
    .sort((a, b) => b.total - a.total),
)

const totalExpenseCats = computed(() =>
  expenseCategories.value.reduce((s, c) => s + c.total, 0),
)
const totalIncomeCats = computed(() =>
  incomeCategories.value.reduce((s, c) => s + c.total, 0),
)

const netClass = computed(() => {
  const net = financeStore.summary.net_balance
  if (net > 0) return 'summary-card--positive'
  if (net < 0) return 'summary-card--negative'
  return ''
})

const maxTotal = computed(() =>
  Math.max(
    financeStore.summary.total_income || 0,
    financeStore.summary.total_expenses || 0,
    1,
  ),
)

const incomeWidth = computed(() =>
  Math.min(100, ((financeStore.summary.total_income || 0) / maxTotal.value) * 100),
)
const expenseWidth = computed(() =>
  Math.min(100, ((financeStore.summary.total_expenses || 0) / maxTotal.value) * 100),
)

const memberSummary = computed(() => {
  const txList = financeStore.transactions
  return FAMILY_MEMBERS.map((name) => {
    const memberTxs = txList.filter((t) => t.member_name === name)
    const income = memberTxs.filter((t) => t.type === 'income').reduce((s, t) => s + t.amount, 0)
    const expense = memberTxs.filter((t) => t.type === 'expense').reduce((s, t) => s + t.amount, 0)
    return { name, income, expense, net: income - expense }
  })
})

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value || 0)
}

function getCatPercent(cat, type) {
  const total = type === 'expense' ? totalExpenseCats.value : totalIncomeCats.value
  if (!total) return 0
  return Math.min(100, (cat.total / total) * 100)
}

async function loadReport() {
  await Promise.all([
    financeStore.fetchSummary(selectedMonth.value, selectedYear.value),
    financeStore.fetchTransactions({ month: selectedMonth.value, year: selectedYear.value }),
  ])
}

onMounted(loadReport)
</script>

<style scoped>
.reports-view {
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

.loading-state,
.empty-state {
  text-align: center;
  padding: 40px;
  color: #9ca3af;
  font-size: 14px;
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
  display: flex;
  align-items: center;
  gap: 16px;
  border-left: 4px solid #e5e7eb;
}

.summary-card--income { border-left-color: #10b981; }
.summary-card--expense { border-left-color: #ef4444; }
.summary-card--positive { border-left-color: #3b82f6; }
.summary-card--negative { border-left-color: #f59e0b; }

.card-icon {
  font-size: 24px;
  font-weight: 700;
  color: #9ca3af;
}

.card-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 4px;
}

.card-amount {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
}

.report-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
  margin-bottom: 16px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.comparison-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 8px;
}

.income-label { color: #059669; }
.expense-label { color: #dc2626; }

.comparison-bar-track {
  height: 20px;
  background: #f3f4f6;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
}

.comparison-bar-income {
  background: #10b981;
  height: 100%;
  transition: width 0.5s;
}

.comparison-bar-expense {
  background: #ef4444;
  height: 100%;
  transition: width 0.5s;
}

.report-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.category-rows {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-row {
  display: grid;
  grid-template-columns: 140px 1fr 100px;
  align-items: center;
  gap: 12px;
}

.cat-info {
  display: flex;
  flex-direction: column;
}

.cat-name {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.cat-count {
  font-size: 11px;
  color: #9ca3af;
}

.cat-bar-track {
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.cat-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.4s;
}

.cat-bar-fill--expense { background: #ef4444; }
.cat-bar-fill--income { background: #10b981; }

.cat-amount {
  font-size: 13px;
  font-weight: 600;
  text-align: right;
}

.amount--income { color: #059669; }
.amount--expense { color: #dc2626; }

.member-table-wrapper {
  overflow-x: auto;
}

.member-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.member-table th {
  padding: 10px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #f3f4f6;
  text-align: left;
}

.text-right { text-align: right; }

.member-table td {
  padding: 12px 14px;
  border-bottom: 1px solid #f3f4f6;
}

.member-badge {
  display: inline-block;
  background: #ede9fe;
  color: #5b21b6;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}
</style>
