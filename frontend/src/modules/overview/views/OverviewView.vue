<template>
  <div class="overview">
    <div class="overview-greeting">
      <div>
        <h1 class="greeting-text">Good {{ timeOfDay }}, {{ firstName }}</h1>
        <p class="greeting-date">{{ formattedDate }}</p>
      </div>
    </div>

    <!-- Alerts + Activity -->
    <div class="overview-top">
      <AlertsPanel :alerts="summary.alerts" :loading="loading" />
      <ActivityFeed :activities="summary.recentActivity" :loading="loading" />
    </div>

    <!-- Module Snapshots -->
    <div class="overview-snapshots">
      <h2 class="section-title">Modules</h2>
      <div class="snapshots-grid">
        <!-- Finance -->
        <ModuleSnapshot icon="💰" label="Finance" route="/finance/dashboard">
          <div class="stat-row">
            <span class="stat-label">This month income</span>
            <span class="stat-value stat-value--income">{{ formatAmount(summary.finance.totalIncome) }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">This month expenses</span>
            <span class="stat-value stat-value--expense">{{ formatAmount(summary.finance.totalExpenses) }}</span>
          </div>
          <div class="stat-row stat-row--total">
            <span class="stat-label">Net balance</span>
            <span class="stat-value" :class="summary.finance.netBalance >= 0 ? 'stat-value--income' : 'stat-value--expense'">
              {{ formatAmount(summary.finance.netBalance) }}
            </span>
          </div>
        </ModuleSnapshot>

        <ModuleSnapshot icon="❤️" label="Health" :coming-soon="true" />
        <ModuleSnapshot icon="📚" label="Education" :coming-soon="true" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/core/auth/auth.store.js'
import { getOverviewSummary } from '../services/overview.service.js'
import AlertsPanel from '../components/AlertsPanel.vue'
import ActivityFeed from '../components/ActivityFeed.vue'
import ModuleSnapshot from '../components/ModuleSnapshot.vue'

const authStore = useAuthStore()
const loading = ref(false)

const summary = ref({
  alerts: [],
  recentActivity: [],
  finance: { totalIncome: 0, totalExpenses: 0, netBalance: 0 },
})

const firstName = computed(() => {
  const user = authStore.user
  const name = user?.user_metadata?.name || user?.email?.split('@')[0] || 'there'
  return name.charAt(0).toUpperCase() + name.slice(1)
})

const timeOfDay = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 17) return 'afternoon'
  return 'evening'
})

const formattedDate = computed(() =>
  new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
)

function formatAmount(amount = 0) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(amount)
}

onMounted(async () => {
  loading.value = true
  try {
    summary.value = await getOverviewSummary()
  } catch (e) {
    // backend may not have data yet — silently use defaults
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.overview {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.overview-greeting {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.greeting-text {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.greeting-date {
  font-size: 14px;
  color: #6b7280;
  margin-top: 2px;
}

.overview-top {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 14px;
}

.snapshots-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid #f3f4f6;
}

.stat-row--total {
  border-bottom: none;
  border-top: 1px solid #e5e7eb;
  padding-top: 10px;
  margin-top: 4px;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
}

.stat-value {
  font-size: 14px;
  font-weight: 700;
  color: #111827;
}

.stat-value--income  { color: #10b981; }
.stat-value--expense { color: #ef4444; }
</style>
