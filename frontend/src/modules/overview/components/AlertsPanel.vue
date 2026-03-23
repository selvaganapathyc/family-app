<template>
  <div class="alerts-panel">
    <h3 class="panel-title">Needs Attention</h3>
    <div v-if="loading" class="state-msg">Loading...</div>
    <div v-else-if="alerts.length === 0" class="state-msg state-msg--good">All clear</div>
    <ul v-else class="alerts-list">
      <li v-for="alert in alerts" :key="alert.id" class="alert-item" :class="`alert-item--${alert.severity}`">
        <span class="alert-icon">{{ alert.icon }}</span>
        <div class="alert-body">
          <span class="alert-text">{{ alert.message }}</span>
          <span class="alert-module">{{ alert.module }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  alerts: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})
</script>

<style scoped>
.alerts-panel {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 20px;
  height: 100%;
}

.panel-title {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
}

.state-msg {
  font-size: 13px;
  color: #9ca3af;
  padding: 8px 0;
}

.state-msg--good {
  color: #10b981;
  font-weight: 500;
}

.alerts-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  border-left: 3px solid transparent;
}

.alert-item--warning {
  background: #fffbeb;
  border-left-color: #f59e0b;
}

.alert-item--danger {
  background: #fef2f2;
  border-left-color: #ef4444;
}

.alert-item--info {
  background: #eff6ff;
  border-left-color: #3b82f6;
}

.alert-icon {
  font-size: 16px;
  margin-top: 1px;
}

.alert-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.alert-text {
  font-size: 13px;
  color: #374151;
  font-weight: 500;
}

.alert-module {
  font-size: 11px;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>
