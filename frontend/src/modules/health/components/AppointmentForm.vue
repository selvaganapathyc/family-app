<script setup>
import { reactive, watch } from 'vue'
import { FAMILY_MEMBERS, MEDICAL_SPECIALTIES } from '../index.js'

const props = defineProps({
  appointment: { type: Object, default: null },
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['submit', 'cancel'])

const today = new Date().toISOString().split('T')[0]

const form = reactive({
  member_name: '',
  doctor_name: '',
  specialty: '',
  date: today,
  time: '',
  status: 'scheduled',
  notes: '',
})

watch(
  () => props.appointment,
  (a) => {
    if (a) {
      form.member_name = a.member_name
      form.doctor_name = a.doctor_name
      form.specialty = a.specialty
      form.date = a.date
      form.time = a.time || ''
      form.status = a.status
      form.notes = a.notes || ''
    } else {
      form.member_name = ''
      form.doctor_name = ''
      form.specialty = ''
      form.date = today
      form.time = ''
      form.status = 'scheduled'
      form.notes = ''
    }
  },
  { immediate: true },
)

function submit() {
  const payload = { ...form }
  if (!payload.time) delete payload.time
  if (!payload.notes) delete payload.notes
  emit('submit', payload)
}
</script>

<template>
  <form class="form" @submit.prevent="submit">
    <div class="field-row">
      <div class="field">
        <label>Family Member</label>
        <select v-model="form.member_name" required>
          <option value="">Select member</option>
          <option v-for="m in FAMILY_MEMBERS" :key="m" :value="m">{{ m }}</option>
        </select>
      </div>
      <div class="field">
        <label>Doctor Name</label>
        <input type="text" v-model="form.doctor_name" required placeholder="Dr. Name" />
      </div>
    </div>

    <div class="field-row">
      <div class="field">
        <label>Specialty</label>
        <select v-model="form.specialty" required>
          <option value="">Select specialty</option>
          <option v-for="s in MEDICAL_SPECIALTIES" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div class="field">
        <label>Status</label>
        <select v-model="form.status">
          <option value="scheduled">Scheduled</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
    </div>

    <div class="field-row">
      <div class="field">
        <label>Date</label>
        <input type="date" v-model="form.date" required />
      </div>
      <div class="field">
        <label>Time <span class="optional">(optional)</span></label>
        <input type="time" v-model="form.time" />
      </div>
    </div>

    <div class="field">
      <label>Notes <span class="optional">(optional)</span></label>
      <input type="text" v-model="form.notes" placeholder="Reason for visit, notes, etc." />
    </div>

    <div class="actions">
      <button type="button" class="btn-secondary" @click="emit('cancel')">Cancel</button>
      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? 'Saving...' : appointment ? 'Update Appointment' : 'Book Appointment' }}
      </button>
    </div>
  </form>
</template>

<style scoped>
.form { display: flex; flex-direction: column; gap: 1rem; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.field { display: flex; flex-direction: column; gap: 0.375rem; }
label { font-size: 0.85rem; font-weight: 500; color: #374151; }
.optional { color: #9ca3af; font-weight: 400; }
input[type="text"], input[type="date"], input[type="time"], select { padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.5rem; font-size: 0.9rem; background: #fff; }
input:focus, select:focus { outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 0.5rem; }
.btn-primary { background: #4f46e5; color: #fff; border: none; padding: 0.5rem 1.25rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #fff; color: #374151; border: 1px solid #d1d5db; padding: 0.5rem 1.25rem; border-radius: 0.5rem; cursor: pointer; }
</style>
