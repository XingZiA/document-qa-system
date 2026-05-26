<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useConversationStore } from '@/stores/conversation'

const chatStore = useChatStore()
const convStore = useConversationStore()
const input = ref('')

async function send() {
  const text = input.value.trim()
  if (!text || chatStore.isStreaming) return
  if (!convStore.activeId) {
    await convStore.create()
  }
  const isFirstMessage = chatStore.messages.length === 0
  input.value = ''
  chatStore.startStream(convStore.activeId!, text)
  if (isFirstMessage) {
    convStore.autoTitle(convStore.activeId!, text)
  }
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}
</script>

<template>
  <div class="chat-input-area">
    <div class="input-wrapper">
      <textarea
        v-model="input"
        placeholder="输入您的问题... (Enter 发送, Shift+Enter 换行)"
        rows="1"
        :disabled="chatStore.isStreaming"
        @keydown="handleKeydown"
      />
      <button
        class="send-btn"
        :disabled="!input.trim() || chatStore.isStreaming"
        @click="send"
      >
        {{ chatStore.isStreaming ? '...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-input-area {
  padding: 16px 24px;
  border-top: 1px solid var(--border);
  background: var(--bg-card);
  flex-shrink: 0;
}

.input-wrapper {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

textarea {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 14px;
  font-family: inherit;
  resize: none;
  outline: none;
  max-height: 120px;
}

textarea:focus {
  border-color: var(--primary);
}

.send-btn {
  padding: 10px 20px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
