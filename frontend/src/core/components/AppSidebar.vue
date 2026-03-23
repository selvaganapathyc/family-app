<template>
  <aside v-if="navLinks.length > 0" class="sidebar">
    <nav class="sidebar-nav">
      <div class="nav-section-title">{{ activeModuleLabel }}</div>
      <router-link
        v-for="item in navLinks"
        :key="item.path"
        :to="item.path"
        class="nav-link"
        active-class="nav-link--active"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-label">{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore, MODULE_NAV, MODULES } from '@/core/store/app.store.js'

const appStore = useAppStore()

const navLinks = computed(() => MODULE_NAV[appStore.activeModule] ?? [])

const activeModuleLabel = computed(() => {
  return MODULES.find((m) => m.key === appStore.activeModule)?.label ?? ''
})
</script>

<style scoped>
.sidebar {
  width: 220px;
  min-width: 220px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 16px 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 0 12px;
}

.nav-section-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: #9ca3af;
  padding: 8px 8px 10px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: 8px;
  text-decoration: none;
  color: #374151;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.15s, color 0.15s;
}

.nav-link:hover {
  background: #f3f4f6;
  color: #111827;
}

.nav-link--active {
  background: linear-gradient(135deg, #667eea15, #764ba215) !important;
  color: #667eea !important;
  font-weight: 600;
}

.nav-icon {
  font-size: 16px;
  width: 20px;
  text-align: center;
}

.nav-label { flex: 1; }
</style>
