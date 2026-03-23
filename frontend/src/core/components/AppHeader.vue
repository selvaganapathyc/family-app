<template>
  <header class="app-header">
    <div class="header-left">
      <span class="header-logo">🏠</span>
      <span class="header-title">Family App</span>
    </div>

    <!-- Module Switcher -->
    <nav class="module-switcher">
      <button
        v-for="mod in MODULES"
        :key="mod.key"
        class="module-tab"
        :class="{
          'module-tab--active': appStore.activeModule === mod.key,
          'module-tab--disabled': mod.comingSoon,
        }"
        :disabled="mod.comingSoon"
        @click="switchModule(mod)"
      >
        <span class="module-tab-icon">{{ mod.icon }}</span>
        <span>{{ mod.label }}</span>
        <span v-if="mod.comingSoon" class="module-tab-soon">Soon</span>
      </button>
    </nav>

    <div class="header-right">
      <div class="user-info">
        <div class="user-avatar">{{ userInitial }}</div>
        <span class="user-name">{{ displayName }}</span>
      </div>
      <button class="logout-btn" :disabled="authStore.loading" @click="handleLogout">
        {{ authStore.loading ? 'Logging out...' : 'Logout' }}
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/core/auth/auth.store.js'
import { useAppStore, MODULES } from '@/core/store/app.store.js'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

const displayName = computed(() => {
  const user = authStore.user
  if (!user) return 'Guest'
  return user.user_metadata?.name || user.email?.split('@')[0] || 'User'
})

const userInitial = computed(() => displayName.value.charAt(0).toUpperCase())

function switchModule(mod) {
  if (mod.comingSoon || !mod.defaultRoute) return
  appStore.setActiveModule(mod.key)
  router.push(mod.defaultRoute)
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-header {
  height: 60px;
  background: #1a1a2e;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 140px;
}

.header-logo { font-size: 22px; }

.header-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

/* Module Switcher */
.module-switcher {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
  justify-content: center;
}

.module-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  background: transparent;
  border: 1px solid transparent;
  color: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.module-tab:hover:not(.module-tab--disabled) {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.module-tab--active {
  background: rgba(255, 255, 255, 0.15) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  color: white !important;
  font-weight: 600;
}

.module-tab--disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

.module-tab-icon { font-size: 15px; }

.module-tab-soon {
  font-size: 9px;
  background: rgba(255,255,255,0.15);
  padding: 1px 5px;
  border-radius: 8px;
  letter-spacing: 0.3px;
}

/* Right side */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 160px;
  justify-content: flex-end;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 34px;
  height: 34px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #e2e8f0;
}

.logout-btn {
  padding: 7px 16px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}

.logout-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.logout-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
