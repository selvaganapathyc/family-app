<script setup>
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '../store/health.store.js'
import { FAMILY_MEMBERS } from '../index.js'
import MedicationForm from '../components/MedicationForm.vue'

const store = useHealthStore()
const showForm = ref(false)
const editingMed = ref(null)

const filterMember = ref('')
const filterActive = ref('')

onMounted(() => store.fetchMedications())

function openAdd() {
  editingMed.value = null
  showForm.value = true
}

function openEdit(m) {
  editingMed.value = { ...m }
  showForm.value = true
}

function cancel() {
  showForm.value = false
  editingMed.value = null
}

async function handleSubmit(data) {
  if (editingMed.value) {
    await store.editMedication(editingMed.value.id, data)
  } else {
    await store.addMedication(data)
  }
  showForm.value = false
  editingMed.value = null
}

async function remove(id) {
  if (confirm('Delete this medication?')) {
    await store.removeMedication(id)
  }
}

async function toggleActive(med) {
  await store.editMedication(med.id, { is_active: !med.is_active })
}

const filtered = computed(() => {
  return store.medications.filter((m) => {
    if (filterMember.value && m.member_name !== filterMember.value) return false
    if (filterActive.value === 'active' && !m.is_active) return false
    if (filterActive.value === 'inactive' && m.is_active) return false
    return true
  })
})

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

const memberColors = { Selva: '#4f46e5', Udhaya: '#db2777', Kayal: '#059669', Kathir: '#d97706' }
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">Medications</h1>
      <button class="btn-primary" @click="openAdd">+ Add Medication</button>
    </div>

    <!-- Form modal -->
    <div v-if="showForm" class="modal-overlay" @click.self="cancel">
      <div class="modal">
        <h2 class="modal-title">{{ editingMed ? 'Edit Medication' : 'Add Medication' }}</h2>
        <MedicationForm
          :medication="editingMed"
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
      <select v-model="filterActive">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>

    <div v-if="store.loading && store.medications.length === 0" class="loading">Loading...</div>

    <div v-else-if="filtered.length === 0" class="empty-state">
      No medications found. Click "Add Medication" to track a prescription.
    </div>

    <div v-else class="table-wrap">
      <table class="table">
        <thead>
          <tr>
            <th>Member</th>
            <th>Medication</th>
            <th>Dosage</th>
            <th>Frequency</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in filtered" :key="m.id" :class="{ inactive: !m.is_active }">
            <td>
              <span class="member-badge" :style="{ background: memberColors[m.member_name] || '#6b7280' }">
                {{ m.member_name }}
              </span>
            </td>
            <td class="med-name">{{ m.name }}</td>
            <td>{{ m.dosage }}</td>
            <td>{{ m.frequency }}</td>
            <td>{{ formatDate(m.start_date) }}</td>
            <td>{{ formatDate(m.end_date) }}</td>
            <td>
              <button
                class="status-badge"
                :class="m.is_active ? 'status-active' : 'status-inactive'"
                @click="toggleActive(m)"
                title="Click to toggle"
              >
                {{ m.is_active ? 'Active' : 'Inactive' }}
              </button>
            </td>
            <td class="actions-cell">
              <button class="btn-edit" @click="openEdit(m)">Edit</button>
              <button class="btn-delete" @click="remove(m.id)">Delete</button>
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
.table tr.inactive td { opacity: 0.55; }
.member-badge { color: #fff; border-radius: 0.375rem; padding: 0.2rem 0.5rem; font-size: 0.75rem; font-weight: 600; }
.med-name { font-weight: 600; color: #111827; }
.status-badge { border: none; border-radius: 9999px; padding: 0.2rem 0.6rem; font-size: 0.75rem; font-weight: 600; cursor: pointer; }
.status-active { background: #dcfce7; color: #16a34a; }
.status-inactive { background: #f3f4f6; color: #9ca3af; }
.actions-cell { display: flex; gap: 0.5rem; }
.btn-primary { background: #4f46e5; color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer; font-size: 0.875rem; }
.btn-edit { background: #f3f4f6; color: #374151; border: none; padding: 0.375rem 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; }
.btn-delete { background: #fee2e2; color: #dc2626; border: none; padding: 0.375rem 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; border-radius: 0.75rem; padding: 1.5rem; width: 100%; max-width: 560px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); }
.modal-title { font-size: 1.125rem; font-weight: 700; margin-bottom: 1.25rem; color: #111827; }
</style>
