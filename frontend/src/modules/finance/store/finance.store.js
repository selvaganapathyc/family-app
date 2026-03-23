import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getTransactions,
  createTransaction,
  updateTransaction as updateTransactionApi,
  deleteTransaction as deleteTransactionApi,
  getBudgets,
  createBudget,
  getSummary,
} from '../services/finance.service.js'

export const useFinanceStore = defineStore('finance', () => {
  const transactions = ref([])
  const budgets = ref([])
  const summary = ref({
    total_income: 0,
    total_expenses: 0,
    net_balance: 0,
    by_category: [],
  })

  const loading = ref(false)
  const error = ref(null)

  // Computed
  const expenses = computed(() =>
    transactions.value.filter((t) => t.type === 'expense'),
  )
  const income = computed(() =>
    transactions.value.filter((t) => t.type === 'income'),
  )

  // ─── Actions ────────────────────────────────────────────────

  async function fetchTransactions(filters = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await getTransactions(filters)
      transactions.value = data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  async function fetchBudgets(month, year) {
    loading.value = true
    error.value = null
    try {
      const data = await getBudgets(month, year)
      budgets.value = data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  async function fetchSummary(month, year) {
    loading.value = true
    error.value = null
    try {
      const data = await getSummary(month, year)
      summary.value = data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  async function addTransaction(data) {
    loading.value = true
    error.value = null
    try {
      const created = await createTransaction(data)
      transactions.value.unshift(created)
      return { data: created, error: null }
    } catch (err) {
      const message = err.response?.data?.detail || err.message
      error.value = message
      return { data: null, error: message }
    } finally {
      loading.value = false
    }
  }

  async function updateTransaction(id, data) {
    loading.value = true
    error.value = null
    try {
      const updated = await updateTransactionApi(id, data)
      const index = transactions.value.findIndex((t) => t.id === id)
      if (index !== -1) {
        transactions.value[index] = updated
      }
      return { data: updated, error: null }
    } catch (err) {
      const message = err.response?.data?.detail || err.message
      error.value = message
      return { data: null, error: message }
    } finally {
      loading.value = false
    }
  }

  async function deleteTransaction(id) {
    loading.value = true
    error.value = null
    try {
      await deleteTransactionApi(id)
      transactions.value = transactions.value.filter((t) => t.id !== id)
      return { error: null }
    } catch (err) {
      const message = err.response?.data?.detail || err.message
      error.value = message
      return { error: message }
    } finally {
      loading.value = false
    }
  }

  async function addOrUpdateBudget(data) {
    loading.value = true
    error.value = null
    try {
      const result = await createBudget(data)
      const index = budgets.value.findIndex(
        (b) =>
          b.category === data.category &&
          b.month === data.month &&
          b.year === data.year,
      )
      if (index !== -1) {
        budgets.value[index] = result
      } else {
        budgets.value.push(result)
      }
      return { data: result, error: null }
    } catch (err) {
      const message = err.response?.data?.detail || err.message
      error.value = message
      return { data: null, error: message }
    } finally {
      loading.value = false
    }
  }

  return {
    transactions,
    budgets,
    summary,
    loading,
    error,
    expenses,
    income,
    fetchTransactions,
    fetchBudgets,
    fetchSummary,
    addTransaction,
    updateTransaction,
    deleteTransaction,
    addOrUpdateBudget,
  }
})
