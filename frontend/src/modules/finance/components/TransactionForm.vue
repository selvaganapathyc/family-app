<template>
  <div class="transaction-form">
    <h3 class="form-title">{{ mode === 'edit' ? 'Edit Transaction' : 'Add Transaction' }}</h3>

    <div v-if="errorMessage" class="error-banner">{{ errorMessage }}</div>

    <form @submit.prevent="handleSubmit">
      <div class="form-grid">
        <!-- Date -->
        <div class="form-group">
          <label class="form-label">Date *</label>
          <input v-model="form.date" type="date" class="form-input" required />
        </div>

        <!-- Type -->
        <div class="form-group">
          <label class="form-label">Type *</label>
          <select v-model="form.type" class="form-input" required>
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>

        <!-- Description -->
        <div class="form-group form-group--full">
          <label class="form-label">Description *</label>
          <input
            v-model="form.description"
            type="text"
            class="form-input"
            placeholder="e.g. Groceries from BigBazaar"
            required
          />
        </div>

        <!-- Amount -->
        <div class="form-group">
          <label class="form-label">Amount (₹) *</label>
          <input
            v-model.number="form.amount"
            type="number"
            class="form-input"
            placeholder="0.00"
            min="0"
            step="0.01"
            required
          />
        </div>

        <!-- Category -->
        <div class="form-group">
          <label class="form-label">Category *</label>
          <select v-model="form.category" class="form-input" required>
            <option value="" disabled>Select category</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>

        <!-- Member -->
        <div class="form-group">
          <label class="form-label">Member *</label>
          <select v-model="form.member_name" class="form-input" required>
            <option value="" disabled>Select member</option>
            <option v-for="member in members" :key="member" :value="member">{{ member }}</option>
          </select>
        </div>
      </div>

      <div class="form-actions">
        <button type="button" class="btn btn--secondary" @click="$emit('cancel')">Cancel</button>
        <button type="submit" class="btn btn--primary" :disabled="loading">
          {{ loading ? 'Saving...' : mode === 'edit' ? 'Update' : 'Add' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { FINANCE_CATEGORIES, FAMILY_MEMBERS } from '../index.js'

const props = defineProps({
  transaction: {
    type: Object,
    default: null,
  },
  mode: {
    type: String,
    default: 'add', // 'add' | 'edit'
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit', 'cancel'])

const categories = FINANCE_CATEGORIES
const members = FAMILY_MEMBERS

const today = new Date().toISOString().split('T')[0]

function defaultForm() {
  return {
    date: today,
    description: '',
    amount: '',
    type: 'expense',
    category: '',
    member_name: '',
  }
}

const form = ref(defaultForm())
const errorMessage = ref('')

// Populate form when editing
watch(
  () => props.transaction,
  (tx) => {
    if (tx) {
      form.value = {
        date: tx.date?.split('T')[0] || today,
        description: tx.description || '',
        amount: tx.amount || '',
        type: tx.type || 'expense',
        category: tx.category || '',
        member_name: tx.member_name || '',
      }
    } else {
      form.value = defaultForm()
    }
  },
  { immediate: true },
)

function handleSubmit() {
  errorMessage.value = ''

  if (!form.value.amount || form.value.amount <= 0) {
    errorMessage.value = 'Amount must be greater than 0.'
    return
  }

  emit('submit', { ...form.value })
}
</script>

<style scoped>
.transaction-form {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.form-title {
  font-size: 17px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 20px;
}

.error-banner {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  color: #c53030;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group--full {
  grid-column: 1 / -1;
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
  color: #111;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  background: white;
}

.form-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn--primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn--primary:hover:not(:disabled) {
  opacity: 0.9;
}

.btn--secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.btn--secondary:hover {
  background: #e5e7eb;
}
</style>
