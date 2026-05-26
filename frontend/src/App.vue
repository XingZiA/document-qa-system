<script setup lang="ts">
import { onMounted } from 'vue'
import { useDocumentStore } from '@/stores/document'
import { useConversationStore } from '@/stores/conversation'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import HomeView from '@/views/HomeView.vue'

const docStore = useDocumentStore()
const convStore = useConversationStore()

onMounted(async () => {
  await Promise.all([docStore.fetchDocuments(), convStore.fetchConversations()])
  if (!convStore.activeId) {
    await convStore.create()
  }
})
</script>

<template>
  <div class="app-container">
    <AppSidebar />
    <div class="main-area">
      <AppHeader />
      <HomeView />
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #4f46e5;
  --primary-light: #818cf8;
  --bg: #f8fafc;
  --bg-sidebar: #f1f5f9;
  --bg-card: #ffffff;
  --border: #e2e8f0;
  --text: #1e293b;
  --text-secondary: #64748b;
  --radius: 8px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
}

.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
