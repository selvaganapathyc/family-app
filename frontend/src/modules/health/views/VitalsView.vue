<script setup>
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '../store/health.store.js'
import { FAMILY_MEMBERS, VITAL_TYPES, VITAL_ICONS } from '../index.js'
import VitalForm from '../components/VitalForm.vue'

const store = useHealthStore()
const showForm = ref(false)
const editingVital = ref(null)

const filterMember = ref('')
const filterType = ref('')

onMounted(() => store.fetchVitals())

function openAdd() {
  editingVital.value = null
  showForm.value = true
}

function openEdit(v) {
  editingVital.value = { ...v }
  showForm.value = true
}

function cancel() {
  showForm.value = false
  editingVital.value = null
}

async function handleSubmit(data) {
  if (editingVital.value) {
    await store.editVital(editingVital.value.id, data)
  } else {
    await store.addVital(data)
  }
  showForm.value = false
  editingVital.value = null
}

async function remove(id) {
  if (confirm('Delete this vital record?')) {
    await store.removeVital(id)
  }
}

const filtered = computed(() => {
  return store.vitals.filter((v) => {
    if (filterMember.value && v.member_name !== filterMember.value) return false
    if (filterType.value && v.vital_type !== filterType.value) return false
    return true
  })
})

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

const memberColors = { Selva: '#4f46e5', Udhaya: '#db2777', Kayal: '#059669', Kathir: '#d97706' }
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">Vitals</h1>
      <button class="btn-primary" @click="openAdd">+ Add Vital</button>
    </div>

    <!-- Form modal -->
    <div v-if="showForm" class="modal-overlay" @click.self="cancel">
      <div class="modal">
        <h2 class="modal-title">{{ editingVital ? 'Edit Vital' : 'Add Vital' }}</h2>
        <VitalForm
          :vital="editingVital"
          :loading="store.loading"
          @submit="handleSubmit"
          @cancel="cancel"
        />
      </div>
    </div>

    <!-- Filters -->
    <div class="filters">
      <select v-model="filterMember">
        <option value="">All Members</option>
        <option v-for="m in FAMILY_MEMBERS" :key="m" :value="m">{{ m }}</option>
      </select>
      <select v-model="filterType">
        <option value="">All Types</option>
        <option v-for="t in VITAL_TYPES" :key="t" :value="t">{{ t }}</option>
      </select>
    </div>

    <div v-if="store.loading && store.vitals.length === 0" class="loading">Loading...</div>

    <div v-else-if="filtered.length === 0" class="empty-state">
      No vitals found. Click "Add Vital" to record your first reading.
    </div>

    <div v-else class="table-wrap">
      <table class="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Member</th>
            <th>Vital</th>
            <th>Value</th>
            <th>Notes</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in filtered" :key="v.id">
            <td>{{ formatDate(v.date) }}</td>
            <td>
              <span class="member-badge" :style="{ background: memberColors[v.member_name] || '#6b7280' }">
                {{ v.member_name }}
              </span>
            </td>
            <td>
              <span class="vital-label">{{ VITAL_ICONS[v.vital_type] || '📊' }} {{ v.vital_type }}</span>
            </td>
            <td class="value-cell">{{ v.value }} {{ v.unit }}</td>
            <td class="notes-cell">{{ v.notes || '—' }}</td>
            <td class="actions-cell">
              <button class="btn-edit" @click="openEdit(v)">Edit</button>
              <button class="btn-delete" @click="remove(v.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page { padding: 2rem; max-width: 1100px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.page-title { font-size: 1.75rem; font-weight: 700; color: #111827; }
.filters { display: flex; gap: 0.75rem; margin-bottom: 1.25rem; }
.filters select { padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.5rem; font-size: 0.875rem; background: #fff; }
.loading, .empty-state { color: #9ca3af; padding: 2rem 0; }
.table-wrap { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.table th { text-align: left; padding: 0.625rem 1rem; background: #f9fafb; border-bottom: 2px solid #e5e7eb; color: #374151; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; }
.table td { padding: 0.75rem 1rem; border-bottom: 1px solid #f3f4f6; color: #374151; vertical-align: middle; }
.member-badge { color: #fff; border-radius: 0.375rem; padding: 0.2rem 0.5rem; font-size: 0.75rem; font-weight: 600; }
.vital-label { display: flex; align-items: center; gap: 0.375rem; }
.value-cell { font-weight: 600; color: #111827; }
.notes-cell { color: #9ca3af; font-size: 0.85rem; max-width: 200px; }
.actions-cell { display: flex; gap: 0.5rem; }
.btn-primary { background: #4f46e5; color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer; font-size: 0.875rem; }
.btn-edit { background: #f3f4f6; color: #374151; border: none; padding: 0.375rem 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; }
.btn-delete { background: #fee2e2; color: #dc2626; border: none; padding: 0.375rem 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; border-radius: 0.75rem; padding: 1.5rem; width: 100%; max-width: 560px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); }
.modal-title { font-size: 1.125rem; font-weight: 700; margin-bottom: 1.25rem; color: #111827; }
</style>
