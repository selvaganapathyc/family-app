<template>
  <div class="activity-feed">
    <h3 class="panel-title">Recent Activity</h3>
    <div v-if="loading" class="state-msg">Loading...</div>
    <div v-else-if="activities.length === 0" class="state-msg">No recent activity</div>
    <ul v-else class="feed-list">
      <li v-for="item in activities" :key="item.id" class="feed-item">
        <div class="feed-avatar">{{ item.memberInitial }}</div>
        <div class="feed-body">
          <p class="feed-text">
            <strong>{{ item.member }}</strong> {{ item.action }}
            <span class="feed-amount" :class="item.type === 'income' ? 'feed-amount--income' : 'feed-amount--expense'">
              {{ item.type === 'income' ? '+' : '-' }}{{ formatAmount(item.amount) }}
            </span>
          </p>
          <p class="feed-meta">{{ item.module }} · {{ item.timeAgo }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  activities: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

function formatAmount(amount) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(amount)
}
</script>

<style scoped>
.activity-feed {
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
}

.feed-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.feed-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.feed-avatar {
  width: 32px;
  height: 32px;
  min-width: 32px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 13px;
  font-weight: 700;
}

.feed-body {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.feed-text {
  font-size: 13px;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.feed-amount {
  font-weight: 700;
  font-size: 13px;
}

.feed-amount--income  { color: #10b981; }
.feed-amount--expense { color: #ef4444; }

.feed-meta {
  font-size: 11px;
  color: #9ca3af;
}
</style>
