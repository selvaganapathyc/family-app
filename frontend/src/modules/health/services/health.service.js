import apiClient from '@/core/api/axios.js'

// ─── Dashboard ───────────────────────────────────────────────────────────────

export async function getDashboard() {
  const response = await apiClient.get('/health/dashboard')
  return response.data
}

// ─── Vitals ──────────────────────────────────────────────────────────────────

export async function getVitals(filters = {}) {
  const response = await apiClient.get('/health/vitals', { params: filters })
  return response.data
}

export async function getLatestVitals() {
  const response = await apiClient.get('/health/vitals/latest')
  return response.data
}

export async function createVital(data) {
  const response = await apiClient.post('/health/vitals', data)
  return response.data
}

export async function updateVital(id, data) {
  const response = await apiClient.put(`/health/vitals/${id}`, data)
  return response.data
}

export async function deleteVital(id) {
  const response = await apiClient.delete(`/health/vitals/${id}`)
  return response.data
}

// ─── Medications ─────────────────────────────────────────────────────────────

export async function getMedications(filters = {}) {
  const response = await apiClient.get('/health/medications', { params: filters })
  return response.data
}

export async function createMedication(data) {
  const response = await apiClient.post('/health/medications', data)
  return response.data
}

export async function updateMedication(id, data) {
  const response = await apiClient.put(`/health/medications/${id}`, data)
  return response.data
}

export async function deleteMedication(id) {
  const response = await apiClient.delete(`/health/medications/${id}`)
  return response.data
}

// ─── Appointments ─────────────────────────────────────────────────────────────

export async function getAppointments(filters = {}) {
  const response = await apiClient.get('/health/appointments', { params: filters })
  return response.data
}

export async function createAppointment(data) {
  const response = await apiClient.post('/health/appointments', data)
  return response.data
}

export async function updateAppointment(id, data) {
  const response = await apiClient.put(`/health/appointments/${id}`, data)
  return response.data
}

export async function deleteAppointment(id) {
  const response = await apiClient.delete(`/health/appointments/${id}`)
  return response.data
}
