<template>
  <div class="expenses-view">
    <div class="page-header">
      <h1 class="page-title">Expenses</h1>
      <button class="btn btn--primary" @click="showForm = !showForm">
        {{ showForm ? 'Cancel' : '+ Add Expense' }}
      </button>
    </div>

    <!-- Add/Edit Form -->
    <TransactionForm
      v-if="showForm"
      :transaction="editingTransaction"
      :mode="editingTransaction ? 'edit' : 'add'"
      :loading="financeStore.loading"
      @submit="handleFormSubmit"
      @cancel="closeForm"
    />

    <!-- Filters -->
    <div class="filters-bar">
      <select v-model="filters.month" class="select-input" @change="loadExpenses">
        <option value="">All Months</option>
        <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
      </select>
      <select v-model="filters.year" class="select-input" @change="loadExpenses">
        <option value="">All Years</option>
        <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
      </select>
      <select v-model="filters.category" class="select-input" @change="loadExpenses">
        <option value="">All Categories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
      <select v-model="filters.member_name" class="select-input" @change="loadExpenses">
        <option value="">All Members</option>
        <option v-for="m in members" :key="m" :value="m">{{ m }}</option>
      </select>
    </div>

    <div v-if="errorMessage" class="error-banner">{{ errorMessage }}</div>

    <!-- Transactions Table -->
    <div class="list-card">
      <TransactionList
        :transactions="filteredExpenses"
        :loading="financeStore.loading"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFinanceStore } from '../store/finance.store.js'
import TransactionList from '../components/TransactionList.vue'
import TransactionForm from '../components/TransactionForm.vue'
import { FINANCE_CATEGORIES, FAMILY_MEMBERS } from '../index.js'

const financeStore = useFinanceStore()

const showForm = ref(false)
const editingTransaction = ref(null)
const errorMessage = ref('')

const categories = FINANCE_CATEGORIES
const members = FAMILY_MEMBERS

const now = new Date()
const filters = ref({
  month: now.getMonth() + 1,
  year: now.getFullYear(),
  category: '',
  member_name: '',
})

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

const filteredExpenses = computed(() => {
  return financeStore.transactions.filter((t) => {
    if (t.type !== 'expense') return false
    if (filters.value.category && t.category !== filters.value.category) return false
    if (filters.value.member_name && t.member_name !== filters.value.member_name) return false
    return true
  })
})

async function loadExpenses() {
  const f = { type: 'expense' }
  if (filters.value.month) f.month = filters.value.month
  if (filters.value.year) f.year = filters.value.year
  await financeStore.fetchTransactions(f)
}

function handleEdit(transaction) {
  editingTransaction.value = transaction
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingTransaction.value = null
  errorMessage.value = ''
}

async function handleFormSubmit(data) {
  errorMessage.value = ''
  const payload = { ...data, type: 'expense' }

  let result
  if (editingTransaction.value) {
    result = await financeStore.updateTransaction(editingTransaction.value.id, payload)
  } else {
    result = await financeStore.addTransaction(payload)
  }

  if (result.error) {
    errorMessage.value = result.error
    return
  }

  closeForm()
}

async function handleDelete(id) {
  const result = await financeStore.deleteTransaction(id)
  if (result.error) errorMessage.value = result.error
}

onMounted(loadExpenses)
</script>

<style scoped>
.expenses-view {
  max-width: 1100px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.filters-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
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

.error-banner {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  color: #c53030;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 14px;
}

.list-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
  overflow: hidden;
}

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

.btn--primary:hover {
  opacity: 0.9;
}
</style>
