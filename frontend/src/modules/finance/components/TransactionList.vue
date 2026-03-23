<template>
  <div class="transaction-list">
    <div v-if="loading" class="loading-state">Loading transactions...</div>

    <div v-else-if="transactions.length === 0" class="empty-state">
      No transactions found.
    </div>

    <div v-else class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Category</th>
            <th>Member</th>
            <th>Type</th>
            <th class="text-right">Amount</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tx in transactions" :key="tx.id" class="table-row">
            <td class="cell-date">{{ formatDate(tx.date) }}</td>
            <td class="cell-desc">{{ tx.description }}</td>
            <td>
              <span class="badge badge--category">{{ tx.category }}</span>
            </td>
            <td>
              <span class="badge badge--member">{{ tx.member_name }}</span>
            </td>
            <td>
              <span class="badge" :class="tx.type === 'income' ? 'badge--income' : 'badge--expense'">
                {{ tx.type }}
              </span>
            </td>
            <td class="cell-amount text-right">
              <span :class="tx.type === 'income' ? 'amount--income' : 'amount--expense'">
                {{ tx.type === 'expense' ? '-' : '+' }}{{ formatCurrency(tx.amount) }}
              </span>
            </td>
            <td class="cell-actions text-center">
              <button class="action-btn action-btn--edit" title="Edit" @click="$emit('edit', tx)">
                ✏️
              </button>
              <button class="action-btn action-btn--delete" title="Delete" @click="handleDelete(tx.id)">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  transactions: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['edit', 'delete'])

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr + 'T00:00:00')
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value || 0)
}

function handleDelete(id) {
  if (window.confirm('Are you sure you want to delete this transaction?')) {
    emit('delete', id)
  }
}
</script>

<style scoped>
.loading-state,
.empty-state {
  text-align: center;
  padding: 40px;
  color: #9ca3af;
  font-size: 14px;
}

.table-wrapper {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.table th {
  text-align: left;
  padding: 10px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #f3f4f6;
  background: #f9fafb;
}

.text-right {
  text-align: right !important;
}

.text-center {
  text-align: center !important;
}

.table-row td {
  padding: 12px 12px;
  border-bottom: 1px solid #f3f4f6;
  color: #374151;
  vertical-align: middle;
}

.table-row:hover td {
  background: #f9fafb;
}

.cell-date {
  white-space: nowrap;
  color: #6b7280;
  font-size: 13px;
}

.cell-desc {
  max-width: 200px;
  font-weight: 500;
  color: #111827;
}

.cell-amount {
  font-weight: 600;
  white-space: nowrap;
}

.amount--income {
  color: #059669;
}

.amount--expense {
  color: #dc2626;
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.badge--income {
  background: #d1fae5;
  color: #065f46;
}

.badge--expense {
  background: #fee2e2;
  color: #991b1b;
}

.badge--category {
  background: #ede9fe;
  color: #5b21b6;
}

.badge--member {
  background: #dbeafe;
  color: #1e40af;
}

.cell-actions {
  white-space: nowrap;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 6px;
  font-size: 15px;
  transition: background 0.15s;
}

.action-btn:hover {
  background: #f3f4f6;
}
</style>
