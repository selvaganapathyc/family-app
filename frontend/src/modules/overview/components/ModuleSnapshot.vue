<template>
  <div class="snapshot-card" :class="{ 'snapshot-card--disabled': comingSoon }" @click="handleClick">
    <div class="snapshot-header">
      <span class="snapshot-icon">{{ icon }}</span>
      <span class="snapshot-label">{{ label }}</span>
      <span v-if="comingSoon" class="coming-soon">Soon</span>
    </div>
    <div v-if="!comingSoon" class="snapshot-body">
      <slot />
    </div>
    <div v-else class="snapshot-placeholder">Coming soon</div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  icon:       { type: String, required: true },
  label:      { type: String, required: true },
  route:      { type: String, default: null },
  comingSoon: { type: Boolean, default: false },
})

const router = useRouter()

function handleClick() {
  if (!props.comingSoon && props.route) {
    router.push(props.route)
  }
}
</script>

<style scoped>
.snapshot-card {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 20px;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
}

.snapshot-card:hover:not(.snapshot-card--disabled) {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.snapshot-card--disabled {
  cursor: default;
  opacity: 0.6;
}

.snapshot-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.snapshot-icon {
  font-size: 20px;
}

.snapshot-label {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  flex: 1;
}

.coming-soon {
  font-size: 10px;
  background: #e5e7eb;
  color: #6b7280;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.snapshot-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.snapshot-placeholder {
  font-size: 13px;
  color: #9ca3af;
  text-align: center;
  padding: 16px 0;
}
</style>
