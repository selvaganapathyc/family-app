<script setup>
import { onMounted, computed } from 'vue'
import { useHealthStore } from '../store/health.store.js'
import { VITAL_ICONS, VITAL_UNITS } from '../index.js'

const store = useHealthStore()

onMounted(() => store.fetchDashboard())

const latestVitals = computed(() => store.dashboard?.latest_vitals ?? [])
const upcomingAppointments = computed(() => store.dashboard?.upcoming_appointments ?? [])
const activeMedications = computed(() => store.dashboard?.active_medications ?? [])

// Group latest vitals by member
const vitalsByMember = computed(() => {
  const map = {}
  for (const v of latestVitals.value) {
    if (!map[v.member_name]) map[v.member_name] = []
    map[v.member_name].push(v)
  }
  return map
})

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

function formatDateTime(d, t) {
  const dateStr = formatDate(d)
  return t ? `${dateStr} at ${t.slice(0, 5)}` : dateStr
}

const memberColors = {
  Selva: '#4f46e5',
  Udhaya: '#db2777',
  Kayal: '#059669',
  Kathir: '#d97706',
}
</script>

<template>
  <div class="dashboard">
    <h1 class="page-title">Health Dashboard</h1>

    <div v-if="store.loading" class="loading">Loading...</div>

    <template v-else>
      <!-- Family Vitals -->
      <section class="section">
        <h2 class="section-title">Latest Vitals</h2>
        <div v-if="Object.keys(vitalsByMember).length === 0" class="empty-state">
          No vitals recorded yet. Go to Vitals to add readings.
        </div>
        <div v-else class="member-grid">
          <div
            v-for="(memberVitals, member) in vitalsByMember"
            :key="member"
            class="member-card"
            :style="{ borderTopColor: memberColors[member] || '#6b7280' }"
          >
            <h3 class="member-name">{{ member }}</h3>
            <div class="vitals-list">
              <div v-for="v in memberVitals" :key="v.id" class="vital-row">
                <span class="vital-icon">{{ VITAL_ICONS[v.vital_type] || '📊' }}</span>
                <span class="vital-label">{{ v.vital_type }}</span>
                <span class="vital-value">{{ v.value }} {{ v.unit }}</span>
                <span class="vital-date">{{ formatDate(v.date) }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Upcoming Appointments -->
      <section class="section">
        <h2 class="section-title">Upcoming Appointments</h2>
        <div v-if="upcomingAppointments.length === 0" class="empty-state">
          No upcoming appointments. Go to Appointments to schedule one.
        </div>
        <div v-else class="appointments-list">
          <div v-for="a in upcomingAppointments" :key="a.id" class="appointment-card">
            <div class="appt-member" :style="{ color: memberColors[a.member_name] || '#6b7280' }">
              {{ a.member_name }}
            </div>
            <div class="appt-doctor">Dr. {{ a.doctor_name }}</div>
            <div class="appt-specialty">{{ a.specialty }}</div>
            <div class="appt-date">{{ formatDateTime(a.date, a.time) }}</div>
          </div>
        </div>
      </section>

      <!-- Active Medications -->
      <section class="section">
        <h2 class="section-title">Active Medications</h2>
        <div v-if="activeMedications.length === 0" class="empty-state">
          No active medications.
        </div>
        <div v-else class="medications-table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Member</th>
                <th>Medication</th>
                <th>Dosage</th>
                <th>Frequency</th>
                <th>Since</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="m in activeMedications" :key="m.id">
                <td>
                  <span class="member-badge" :style="{ background: memberColors[m.member_name] || '#6b7280' }">
                    {{ m.member_name }}
                  </span>
                </td>
                <td>{{ m.name }}</td>
                <td>{{ m.dosage }}</td>
                <td>{{ m.frequency }}</td>
                <td>{{ formatDate(m.start_date) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.dashboard { padding: 2rem; max-width: 1100px; }
.page-title { font-size: 1.75rem; font-weight: 700; margin-bottom: 2rem; color: #111827; }
.section { margin-bottom: 2.5rem; }
.section-title { font-size: 1.125rem; font-weight: 600; color: #374151; margin-bottom: 1rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.5rem; }
.empty-state { color: #9ca3af; font-size: 0.9rem; padding: 1rem 0; }
.loading { color: #6b7280; padding: 2rem; }

.member-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1rem; }
.member-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 0.75rem; border-top: 4px solid #6b7280; padding: 1rem; }
.member-name { font-weight: 600; font-size: 1rem; margin-bottom: 0.75rem; color: #111827; }
.vitals-list { display: flex; flex-direction: column; gap: 0.5rem; }
.vital-row { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; }
.vital-icon { font-size: 1rem; }
.vital-label { color: #6b7280; flex: 1; }
.vital-value { font-weight: 600; color: #111827; }
.vital-date { color: #d1d5db; font-size: 0.75rem; }

.appointments-list { display: flex; flex-wrap: wrap; gap: 0.75rem; }
.appointment-card { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 0.75rem; padding: 0.875rem 1rem; min-width: 200px; }
.appt-member { font-weight: 700; font-size: 0.85rem; margin-bottom: 0.25rem; }
.appt-doctor { font-weight: 600; color: #111827; }
.appt-specialty { font-size: 0.8rem; color: #6b7280; margin-bottom: 0.25rem; }
.appt-date { font-size: 0.8rem; color: #059669; font-weight: 500; }

.medications-table-wrap { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.table th { text-align: left; padding: 0.625rem 1rem; background: #f9fafb; border-bottom: 2px solid #e5e7eb; color: #374151; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; }
.table td { padding: 0.75rem 1rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
.member-badge { color: #fff; border-radius: 0.375rem; padding: 0.2rem 0.5rem; font-size: 0.75rem; font-weight: 600; }
</style>
