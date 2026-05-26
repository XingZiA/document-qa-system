<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import ChatMessage from './ChatMessage.vue'

const chatStore = useChatStore()
const container = ref<HTMLElement | null>(null)

watch(
  () => [chatStore.messages.length, chatStore.streamingContent],
  async () => {
    await nextTick()
    if (container.value) {
      container.value.scrollTop = container.value.scrollHeight
    }
  },
  { deep: true }
)
</script>

<template>
  <div
    ref="container"
    class="chat-window"
  >
    <div
      v-if="chatStore.messages.length === 0 && !chatStore.isStreaming"
      class="empty-state"
    >
      <div class="empty-icon">
        &#128214;
      </div>
      <h2>文档问答助手</h2>
      <p>上传文档后开始提问，支持 PDF、Word、TXT、Markdown</p>
    </div>

    <div class="messages">
      <ChatMessage
        v-for="msg in chatStore.messages"
        :key="msg.id"
        :role="msg.role"
        :content="msg.content"
        :is-streaming="false"
      />
      <ChatMessage
        v-if="chatStore.isStreaming && chatStore.streamingContent"
        role="assistant"
        :content="chatStore.streamingContent"
        :is-streaming="true"
      />
    </div>
  </div>
</template>

<style scoped>
.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-secondary);
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state h2 {
  font-size: 22px;
  margin-bottom: 8px;
  color: var(--text);
}

.empty-state p {
  font-size: 14px;
}

.messages {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
