import apiClient from '@/core/api/axios.js'

export async function getOverviewSummary() {
  const { data } = await apiClient.get('/overview/summary')
  return data
}
