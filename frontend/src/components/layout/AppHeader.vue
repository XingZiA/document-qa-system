<script setup lang="ts">
import { useConversationStore } from '@/stores/conversation'

const convStore = useConversationStore()
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <h1 class="logo">
        RAG智能问答系统
      </h1>
    </div>
    <div class="header-right">
      <span class="conv-title">{{ convStore.conversations.find(c => c.id === convStore.activeId)?.title || 'New Chat' }}</span>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-card);
  flex-shrink: 0;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary);
}

.conv-title {
  font-size: 14px;
  color: var(--text-secondary);
}
</style>
