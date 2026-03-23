<script setup>
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '../store/health.store.js'
import { FAMILY_MEMBERS } from '../index.js'
import AppointmentForm from '../components/AppointmentForm.vue'

const store = useHealthStore()
const showForm = ref(false)
const editingAppt = ref(null)

const filterMember = ref('')
const filterStatus = ref('')

onMounted(() => store.fetchAppointments())

function openAdd() {
  editingAppt.value = null
  showForm.value = true
}

function openEdit(a) {
  editingAppt.value = { ...a }
  showForm.value = true
}

function cancel() {
  showForm.value = false
  editingAppt.value = null
}

async function handleSubmit(data) {
  if (editingAppt.value) {
    await store.editAppointment(editingAppt.value.id, data)
  } else {
    await store.addAppointment(data)
  }
  showForm.value = false
  editingAppt.value = null
}

async function remove(id) {
  if (confirm('Delete this appointment?')) {
    await store.removeAppointment(id)
  }
}

async function markCompleted(a) {
  await store.editAppointment(a.id, { status: 'completed' })
}

const filtered = computed(() => {
  return store.appointments.filter((a) => {
    if (filterMember.value && a.member_name !== filterMember.value) return false
    if (filterStatus.value && a.status !== filterStatus.value) return false
    return true
  })
})

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

function formatTime(t) {
  if (!t) return ''
  const [h, m] = t.split(':')
  const hour = parseInt(h)
  return `${hour > 12 ? hour - 12 : hour || 12}:${m} ${hour >= 12 ? 'PM' : 'AM'}`
}

const statusConfig = {
  scheduled: { label: 'Scheduled', class: 'status-scheduled' },
  completed: { label: 'Completed', class: 'status-completed' },
  cancelled: { label: 'Cancelled', class: 'status-cancelled' },
}

const memberColors = { Selva: '#4f46e5', Udhaya: '#db2777', Kayal: '#059669', Kathir: '#d97706' }
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">Appointments</h1>
      <button class="btn-primary" @click="openAdd">+ Book Appointment</button>
    </div>

    <!-- Form modal -->
    <div v-if="showForm" class="modal-overlay" @click.self="cancel">
      <div class="modal">
        <h2 class="modal-title">{{ editingAppt ? 'Edit Appointment' : 'Book Appointment' }}</h2>
        <AppointmentForm
          :appointment="editingAppt"
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
      <select v-model="filterStatus">
        <option value="">All Status</option>
        <option value="scheduled">Scheduled</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>
    </div>

    <div v-if="store.loading && store.appointments.length === 0" class="loading">Loading...</div>

    <div v-else-if="filtered.length === 0" class="empty-state">
      No appointments found. Click "Book Appointment" to schedule a visit.
    </div>

    <div v-else class="appointments-grid">
      <div
        v-for="a in filtered"
        :key="a.id"
        class="appt-card"
        :class="`card-${a.status}`"
      >
        <div class="card-top">
          <span class="member-badge" :style="{ background: memberColors[a.member_name] || '#6b7280' }">
            {{ a.member_name }}
          </span>
          <span class="status-badge" :class="statusConfig[a.status]?.class">
            {{ statusConfig[a.status]?.label }}
          </span>
        </div>

        <div class="card-doctor">Dr. {{ a.doctor_name }}</div>
        <div class="card-specialty">{{ a.specialty }}</div>

        <div class="card-datetime">
          {{ formatDate(a.date) }}
          <span v-if="a.time"> · {{ formatTime(a.time) }}</span>
        </div>

        <div v-if="a.notes" class="card-notes">{{ a.notes }}</div>

        <div class="card-actions">
          <button
            v-if="a.status === 'scheduled'"
            class="btn-complete"
            @click="markCompleted(a)"
          >
            Mark Completed
          </button>
          <button class="btn-edit" @click="openEdit(a)">Edit</button>
          <button class="btn-delete" @click="remove(a.id)">Delete</button>
        </div>
      </div>
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

.appointments-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }

.appt-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem 1.125rem; display: flex; flex-direction: column; gap: 0.375rem; }
.card-scheduled { border-left: 4px solid #6366f1; }
.card-completed { border-left: 4px solid #16a34a; opacity: 0.8; }
.card-cancelled { border-left: 4px solid #9ca3af; opacity: 0.6; }

.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem; }
.member-badge { color: #fff; border-radius: 0.375rem; padding: 0.2rem 0.5rem; font-size: 0.75rem; font-weight: 600; }
.status-badge { border-radius: 9999px; padding: 0.2rem 0.6rem; font-size: 0.75rem; font-weight: 600; }
.status-scheduled { background: #e0e7ff; color: #4338ca; }
.status-completed { background: #dcfce7; color: #16a34a; }
.status-cancelled { background: #f3f4f6; color: #9ca3af; }

.card-doctor { font-weight: 700; font-size: 1rem; color: #111827; }
.card-specialty { font-size: 0.85rem; color: #6b7280; }
.card-datetime { font-size: 0.875rem; color: #4f46e5; font-weight: 500; margin-top: 0.25rem; }
.card-notes { font-size: 0.8rem; color: #9ca3af; margin-top: 0.125rem; }

.card-actions { display: flex; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap; }
.btn-primary { background: #4f46e5; color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer; font-size: 0.875rem; }
.btn-complete { background: #dcfce7; color: #16a34a; border: none; padding: 0.375rem 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; font-weight: 500; }
.btn-edit { background: #f3f4f6; color: #374151; border: none; padding: 0.375rem 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; }
.btn-delete { background: #fee2e2; color: #dc2626; border: none; padding: 0.375rem 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; border-radius: 0.75rem; padding: 1.5rem; width: 100%; max-width: 560px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); }
.modal-title { font-size: 1.125rem; font-weight: 700; margin-bottom: 1.25rem; color: #111827; }
</style>
