import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as healthService from '../services/health.service.js'

export const useHealthStore = defineStore('health', () => {
  const vitals = ref([])
  const medications = ref([])
  const appointments = ref([])
  const dashboard = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // ─── Dashboard ─────────────────────────────────────────────────────────────

  async function fetchDashboard() {
    loading.value = true
    error.value = null
    try {
      dashboard.value = await healthService.getDashboard()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  // ─── Vitals ────────────────────────────────────────────────────────────────

  async function fetchVitals(filters = {}) {
    loading.value = true
    error.value = null
    try {
      vitals.value = await healthService.getVitals(filters)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function addVital(data) {
    loading.value = true
    error.value = null
    try {
      const newVital = await healthService.createVital(data)
      vitals.value.unshift(newVital)
      return newVital
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function editVital(id, data) {
    loading.value = true
    error.value = null
    try {
      const updated = await healthService.updateVital(id, data)
      const idx = vitals.value.findIndex((v) => v.id === id)
      if (idx !== -1) vitals.value[idx] = updated
      return updated
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function removeVital(id) {
    loading.value = true
    error.value = null
    try {
      await healthService.deleteVital(id)
      vitals.value = vitals.value.filter((v) => v.id !== id)
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  // ─── Medications ───────────────────────────────────────────────────────────

  async function fetchMedications(filters = {}) {
    loading.value = true
    error.value = null
    try {
      medications.value = await healthService.getMedications(filters)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function addMedication(data) {
    loading.value = true
    error.value = null
    try {
      const newMed = await healthService.createMedication(data)
      medications.value.unshift(newMed)
      return newMed
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function editMedication(id, data) {
    loading.value = true
    error.value = null
    try {
      const updated = await healthService.updateMedication(id, data)
      const idx = medications.value.findIndex((m) => m.id === id)
      if (idx !== -1) medications.value[idx] = updated
      return updated
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function removeMedication(id) {
    loading.value = true
    error.value = null
    try {
      await healthService.deleteMedication(id)
      medications.value = medications.value.filter((m) => m.id !== id)
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  // ─── Appointments ──────────────────────────────────────────────────────────

  async function fetchAppointments(filters = {}) {
    loading.value = true
    error.value = null
    try {
      appointments.value = await healthService.getAppointments(filters)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function addAppointment(data) {
    loading.value = true
    error.value = null
    try {
      const newAppt = await healthService.createAppointment(data)
      appointments.value.unshift(newAppt)
      return newAppt
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function editAppointment(id, data) {
    loading.value = true
    error.value = null
    try {
      const updated = await healthService.updateAppointment(id, data)
      const idx = appointments.value.findIndex((a) => a.id === id)
      if (idx !== -1) appointments.value[idx] = updated
      return updated
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function removeAppointment(id) {
    loading.value = true
    error.value = null
    try {
      await healthService.deleteAppointment(id)
      appointments.value = appointments.value.filter((a) => a.id !== id)
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    vitals, medications, appointments, dashboard, loading, error,
    fetchDashboard,
    fetchVitals, addVital, editVital, removeVital,
    fetchMedications, addMedication, editMedication, removeMedication,
    fetchAppointments, addAppointment, editAppointment, removeAppointment,
  }
})
