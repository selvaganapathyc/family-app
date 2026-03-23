import apiClient from '@/core/api/axios.js'

/**
 * Fetch transactions with optional filters.
 * @param {Object} filters - { month, year, type, member_name }
 */
export async function getTransactions(filters = {}) {
  const params = {}
  if (filters.month) params.month = filters.month
  if (filters.year) params.year = filters.year
  if (filters.type) params.type = filters.type
  if (filters.member_name) params.member = filters.member_name

  const response = await apiClient.get('/finance/transactions', { params })
  return response.data
}

/**
 * Create a new transaction.
 * @param {Object} data - { date, description, amount, type, category, member_name }
 */
export async function createTransaction(data) {
  const response = await apiClient.post('/finance/transactions', data)
  return response.data
}

/**
 * Update an existing transaction.
 * @param {string} id - Transaction UUID
 * @param {Object} data - Partial transaction fields
 */
export async function updateTransaction(id, data) {
  const response = await apiClient.put(`/finance/transactions/${id}`, data)
  return response.data
}

/**
 * Delete a transaction.
 * @param {string} id - Transaction UUID
 */
export async function deleteTransaction(id) {
  const response = await apiClient.delete(`/finance/transactions/${id}`)
  return response.data
}

/**
 * Fetch budgets for a given month/year.
 * @param {number} month
 * @param {number} year
 */
export async function getBudgets(month, year) {
  const response = await apiClient.get('/finance/budgets', {
    params: { month, year },
  })
  return response.data
}

/**
 * Create or update a budget entry.
 * @param {Object} data - { month, year, category, amount }
 */
export async function createBudget(data) {
  const response = await apiClient.post('/finance/budgets', data)
  return response.data
}

/**
 * Fetch the monthly financial summary.
 * @param {number} month
 * @param {number} year
 */
export async function getSummary(month, year) {
  const response = await apiClient.get('/finance/summary', {
    params: { month, year },
  })
  return response.data
}
