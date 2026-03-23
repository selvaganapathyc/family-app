<template>
  <div class="budget-view">
    <div class="page-header">
      <h1 class="page-title">Budget</h1>
      <div class="header-controls">
        <select v-model="selectedMonth" class="select-input" @change="loadData">
          <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
        </select>
        <select v-model="selectedYear" class="select-input" @change="loadData">
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
        <button class="btn btn--primary" @click="showForm = true">+ Set Budget</button>
      </div>
    </div>

    <!-- Add/Edit Budget Form -->
    <div v-if="showForm" class="budget-form-card">
      <h3 class="form-title">{{ editingBudget ? 'Edit Budget' : 'Set Budget' }}</h3>
      <div v-if="formError" class="error-banner">{{ formError }}</div>
      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">Category *</label>
          <select v-model="budgetForm.category" class="form-input" required>
            <option value="" disabled>Select category</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Budget Amount (₹) *</label>
          <input
            v-model.number="budgetForm.amount"
            type="number"
            class="form-input"
            min="0"
            step="1"
            placeholder="0"
          />
        </div>
      </div>
      <div class="form-actions">
        <button class="btn btn--secondary" @click="closeForm">Cancel</button>
        <button class="btn btn--primary" :disabled="financeStore.loading" @click="handleBudgetSubmit">
          {{ financeStore.loading ? 'Saving...' : 'Save Budget' }}
        </button>
      </div>
    </div>

    <!-- Budget List -->
    <div v-if="financeStore.loading && !financeStore.budgets.length" class="loading-state">
      Loading budgets...
    </div>
    <div v-else-if="financeStore.budgets.length === 0" class="empty-state">
      No budgets set for {{ selectedMonthLabel }} {{ selectedYear }}.
      Click "Set Budget" to add one.
    </div>
    <div v-else class="budget-grid">
      <div v-for="budget in financeStore.budgets" :key="budget.id" class="budget-card">
        <div class="budget-card-header">
          <span class="budget-category">{{ budget.category }}</span>
          <button class="edit-btn" title="Edit budget" @click="handleEditBudget(budget)">✏️</button>
        </div>

        <div class="budget-amounts">
          <div class="spent-amount" :class="isOverBudget(budget) ? 'over' : ''">
            {{ formatCurrency(budget.spent || 0) }}
            <span class="spent-label">spent</span>
          </div>
          <div class="budget-total">
            of {{ formatCurrency(budget.amount) }}
          </div>
        </div>

        <div class="budget-bar-track">
          <div
            class="budget-bar-fill"
            :class="getBudgetBarClass(budget)"
            :style="{ width: getBudgetPercent(budget) + '%' }"
          ></div>
        </div>

        <div class="budget-footer">
          <span :class="isOverBudget(budget) ? 'text-danger' : 'text-muted'">
            {{ getRemainingLabel(budget) }}
          </span>
          <span class="budget-pct">{{ getBudgetPercent(budget).toFixed(0) }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '../store/finance.store.js'
import { FINANCE_CATEGORIES } from '../index.js'

const financeStore = useFinanceStore()
const categories = FINANCE_CATEGORIES

const now = new Date()
const selectedMonth = ref(now.getMonth() + 1)
const selectedYear = ref(now.getFullYear())
const showForm = ref(false)
const editingBudget = ref(null)
const formError = ref('')

const budgetForm = ref({ category: '', amount: '' })

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

const selectedMonthLabel = computed(
  () => months.find((m) => m.value === selectedMonth.value)?.label || '',
)

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

function isOverBudget(budget) {
  return (budget.spent || 0) > budget.amount
}

function getRemainingLabel(budget) {
  const remaining = budget.amount - (budget.spent || 0)
  if (remaining < 0) return `Over by ${formatCurrency(Math.abs(remaining))}`
  return `${formatCurrency(remaining)} remaining`
}

function handleEditBudget(budget) {
  editingBudget.value = budget
  budgetForm.value = { category: budget.category, amount: budget.amount }
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingBudget.value = null
  budgetForm.value = { category: '', amount: '' }
  formError.value = ''
}

async function handleBudgetSubmit() {
  formError.value = ''
  if (!budgetForm.value.category || !budgetForm.value.amount) {
    formError.value = 'Category and amount are required.'
    return
  }
  const payload = {
    category: budgetForm.value.category,
    amount: budgetForm.value.amount,
    month: selectedMonth.value,
    year: selectedYear.value,
  }
  const result = await financeStore.addOrUpdateBudget(payload)
  if (result.error) {
    formError.value = result.error
    return
  }
  closeForm()
  await loadData()
}

async function loadData() {
  await Promise.all([
    financeStore.fetchBudgets(selectedMonth.value, selectedYear.value),
    financeStore.fetchTransactions({ month: selectedMonth.value, year: selectedYear.value }),
  ])
}

onMounted(loadData)
</script>

<style scoped>
.budget-view {
  max-width: 1100px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.header-controls {
  display: flex;
  gap: 10px;
  align-items: center;
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

.budget-form-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.form-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #111827;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.form-input {
  padding: 9px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  background: white;
}

.form-input:focus {
  border-color: #667eea;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.error-banner {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  color: #c53030;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 14px;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px;
  color: #9ca3af;
  font-size: 14px;
  background: white;
  border-radius: 12px;
}

.budget-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.budget-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
}

.budget-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.budget-category {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.edit-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 4px 6px;
  border-radius: 6px;
}

.edit-btn:hover {
  background: #f3f4f6;
}

.budget-amounts {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 10px;
}

.spent-amount {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
}

.spent-amount.over {
  color: #dc2626;
}

.spent-label {
  font-size: 12px;
  font-weight: 400;
  color: #9ca3af;
}

.budget-total {
  font-size: 13px;
  color: #6b7280;
}

.budget-bar-track {
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.budget-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.4s ease;
}

.bar--ok { background: #10b981; }
.bar--warn { background: #f59e0b; }
.bar--over { background: #ef4444; }

.budget-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.text-muted { color: #9ca3af; }
.text-danger { color: #dc2626; font-weight: 500; }
.budget-pct { color: #6b7280; }

.btn {
  padding: 9px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

.btn--primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn--primary:hover:not(:disabled) { opacity: 0.9; }
.btn--primary:disabled { opacity: 0.6; cursor: not-allowed; }

.btn--secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.btn--secondary:hover { background: #e5e7eb; }
</style>
