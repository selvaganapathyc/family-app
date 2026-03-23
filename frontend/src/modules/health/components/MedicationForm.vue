<script setup>
import { reactive, watch } from 'vue'
import { FAMILY_MEMBERS, MEDICATION_FREQUENCIES } from '../index.js'

const props = defineProps({
  medication: { type: Object, default: null },
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['submit', 'cancel'])

const today = new Date().toISOString().split('T')[0]

const form = reactive({
  member_name: '',
  name: '',
  dosage: '',
  frequency: '',
  start_date: today,
  end_date: '',
  is_active: true,
  notes: '',
})

watch(
  () => props.medication,
  (m) => {
    if (m) {
      form.member_name = m.member_name
      form.name = m.name
      form.dosage = m.dosage
      form.frequency = m.frequency
      form.start_date = m.start_date
      form.end_date = m.end_date || ''
      form.is_active = m.is_active
      form.notes = m.notes || ''
    } else {
      form.member_name = ''
      form.name = ''
      form.dosage = ''
      form.frequency = ''
      form.start_date = today
      form.end_date = ''
      form.is_active = true
      form.notes = ''
    }
  },
  { immediate: true },
)

function submit() {
  const payload = { ...form }
  if (!payload.end_date) delete payload.end_date
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
        <label>Medication Name</label>
        <input type="text" v-model="form.name" required placeholder="e.g. Paracetamol" />
      </div>
    </div>

    <div class="field-row">
      <div class="field">
        <label>Dosage</label>
        <input type="text" v-model="form.dosage" required placeholder="e.g. 500mg" />
      </div>
      <div class="field">
        <label>Frequency</label>
        <select v-model="form.frequency" required>
          <option value="">Select frequency</option>
          <option v-for="f in MEDICATION_FREQUENCIES" :key="f" :value="f">{{ f }}</option>
        </select>
      </div>
    </div>

    <div class="field-row">
      <div class="field">
        <label>Start Date</label>
        <input type="date" v-model="form.start_date" required />
      </div>
      <div class="field">
        <label>End Date <span class="optional">(optional)</span></label>
        <input type="date" v-model="form.end_date" />
      </div>
    </div>

    <div class="field-row">
      <div class="field">
        <label>Notes <span class="optional">(optional)</span></label>
        <input type="text" v-model="form.notes" placeholder="Any additional notes" />
      </div>
      <div class="field field-checkbox">
        <label class="checkbox-label">
          <input type="checkbox" v-model="form.is_active" />
          Currently active
        </label>
      </div>
    </div>

    <div class="actions">
      <button type="button" class="btn-secondary" @click="emit('cancel')">Cancel</button>
      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? 'Saving...' : medication ? 'Update Medication' : 'Add Medication' }}
      </button>
    </div>
  </form>
</template>

<style scoped>
.form { display: flex; flex-direction: column; gap: 1rem; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.field { display: flex; flex-direction: column; gap: 0.375rem; }
.field-checkbox { justify-content: flex-end; padding-bottom: 0.25rem; }
.checkbox-label { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: #374151; cursor: pointer; }
label { font-size: 0.85rem; font-weight: 500; color: #374151; }
.optional { color: #9ca3af; font-weight: 400; }
input[type="text"], input[type="date"], select { padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.5rem; font-size: 0.9rem; background: #fff; }
input:focus, select:focus { outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 0.5rem; }
.btn-primary { background: #4f46e5; color: #fff; border: none; padding: 0.5rem 1.25rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #fff; color: #374151; border: 1px solid #d1d5db; padding: 0.5rem 1.25rem; border-radius: 0.5rem; cursor: pointer; }
</style>
