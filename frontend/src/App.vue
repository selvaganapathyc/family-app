<template>
  <div id="app-root">
    <template v-if="authStore.isAuthenticated">
      <AppHeader />
      <div class="app-layout">
        <AppSidebar />
        <main class="app-main">
          <router-view />
        </main>
      </div>
    </template>
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/core/auth/auth.store.js'
import { useAppStore } from '@/core/store/app.store.js'
import AppHeader from '@/core/components/AppHeader.vue'
import AppSidebar from '@/core/components/AppSidebar.vue'

const authStore = useAuthStore()
const appStore = useAppStore()
const route = useRoute()

// Keep activeModule in sync when user navigates directly via URL
watch(() => route.path, (path) => appStore.syncFromRoute(path), { immediate: true })

onMounted(async () => {
  await authStore.initAuth()
})
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  background-color: #f5f7fa;
  color: #333;
}

#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-layout {
  display: flex;
  flex: 1;
  min-height: calc(100vh - 60px);
}

.app-main {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}
</style>
