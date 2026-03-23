<script setup>
import { reactive, watch } from 'vue'
import { FAMILY_MEMBERS, VITAL_TYPES, VITAL_UNITS } from '../index.js'

const props = defineProps({
  vital: { type: Object, default: null },
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['submit', 'cancel'])

const today = new Date().toISOString().split('T')[0]

const form = reactive({
  member_name: '',
  date: today,
  vital_type: '',
  value: '',
  unit: '',
  notes: '',
})

watch(
  () => props.vital,
  (v) => {
    if (v) {
      form.member_name = v.member_name
      form.date = v.date
      form.vital_type = v.vital_type
      form.value = v.value
      form.unit = v.unit
      form.notes = v.notes || ''
    } else {
      form.member_name = ''
      form.date = today
      form.vital_type = ''
      form.value = ''
      form.unit = ''
      form.notes = ''
    }
  },
  { immediate: true },
)

function onVitalTypeChange() {
  form.unit = VITAL_UNITS[form.vital_type] || ''
}

function submit() {
  emit('submit', { ...form, value: parseFloat(form.value) })
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
        <label>Date</label>
        <input type="date" v-model="form.date" required />
      </div>
    </div>

    <div class="field-row">
      <div class="field">
        <label>Vital Type</label>
        <select v-model="form.vital_type" @change="onVitalTypeChange" required>
          <option value="">Select type</option>
          <option v-for="t in VITAL_TYPES" :key="t" :value="t">{{ t }}</option>
        </select>
      </div>
      <div class="field">
        <label>Value</label>
        <div class="input-with-unit">
          <input type="number" v-model="form.value" step="0.01" min="0.01" required placeholder="0.00" />
          <span class="unit-badge">{{ form.unit || '—' }}</span>
        </div>
      </div>
    </div>

    <div class="field">
      <label>Notes <span class="optional">(optional)</span></label>
      <input type="text" v-model="form.notes" placeholder="Any additional notes" />
    </div>

    <div class="actions">
      <button type="button" class="btn-secondary" @click="emit('cancel')">Cancel</button>
      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? 'Saving...' : vital ? 'Update Vital' : 'Add Vital' }}
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
input, select { padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.5rem; font-size: 0.9rem; background: #fff; }
input:focus, select:focus { outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.input-with-unit { display: flex; align-items: center; gap: 0.5rem; }
.input-with-unit input { flex: 1; }
.unit-badge { font-size: 0.8rem; color: #6b7280; background: #f3f4f6; padding: 0.375rem 0.625rem; border-radius: 0.375rem; white-space: nowrap; border: 1px solid #e5e7eb; }
.actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 0.5rem; }
.btn-primary { background: #4f46e5; color: #fff; border: none; padding: 0.5rem 1.25rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #fff; color: #374151; border: 1px solid #d1d5db; padding: 0.5rem 1.25rem; border-radius: 0.5rem; cursor: pointer; }
</style>
