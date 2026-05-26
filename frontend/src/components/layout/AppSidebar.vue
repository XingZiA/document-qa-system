<script setup lang="ts">
import { useConversationStore } from '@/stores/conversation'
import { useChatStore } from '@/stores/chat'
import DocumentCard from '@/components/document/DocumentCard.vue'
import DocumentUpload from '@/components/document/DocumentUpload.vue'
import { ref } from 'vue'

const convStore = useConversationStore()
const chatStore = useChatStore()
const showUpload = ref(false)
const editingId = ref<number | null>(null)
const editTitle = ref('')

async function selectConversation(id: number) {
  convStore.setActive(id)
  await chatStore.loadMessages(id)
}

async function newChat() {
  chatStore.clear()
  await convStore.create()
}

function startEdit(conv: { id: number; title: string }) {
  editingId.value = conv.id
  editTitle.value = conv.title
}

async function confirmEdit() {
  const trimmed = editTitle.value.trim()
  if (trimmed && editingId.value !== null) {
    await convStore.rename(editingId.value, trimmed)
  }
  editingId.value = null
}

function cancelEdit() {
  editingId.value = null
}

function handleEditKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter') {
    e.preventDefault()
    confirmEdit()
  } else if (e.key === 'Escape') {
    cancelEdit()
  }
}
</script>

<template>
  <aside class="sidebar">
    <button
      class="new-chat-btn"
      @click="newChat"
    >
      + 新对话
    </button>

    <div class="section">
      <h3 class="section-title">
        对话历史
      </h3>
      <div class="list">
        <div
          v-for="conv in convStore.conversations"
          :key="conv.id"
          class="list-item"
          :class="{ active: conv.id === convStore.activeId, editing: editingId === conv.id }"
          @click="selectConversation(conv.id)"
          @dblclick="startEdit(conv)"
        >
          <input
            v-if="editingId === conv.id"
            v-model="editTitle"
            class="edit-input"
            @keydown="handleEditKeydown"
            @blur="confirmEdit"
            @click.stop
          >
          <span
            v-else
            class="item-text"
          >{{ conv.title }}</span>
          <button
            class="del-btn"
            @click.stop="convStore.remove(conv.id)"
          >
            ×
          </button>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-header">
        <h3 class="section-title">
          文档列表
        </h3>
        <button
          class="upload-btn"
          @click="showUpload = true"
        >
          +
        </button>
      </div>
      <DocumentCard />
    </div>

    <DocumentUpload
      v-if="showUpload"
      @close="showUpload = false"
    />
  </aside>
</template>

<style scoped>
.sidebar {
  width: 280px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 12px;
  gap: 16px;
  overflow-y: auto;
  flex-shrink: 0;
}

.new-chat-btn {
  width: 100%;
  padding: 10px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.new-chat-btn:hover {
  background: var(--primary-light);
}

.section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 12px;
  text-transform: uppercase;
  color: var(--text-secondary);
  letter-spacing: 0.5px;
}

.upload-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--bg-card);
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.list-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text);
}

.list-item:hover {
  background: rgba(0,0,0,0.05);
}

.list-item.active {
  background: var(--primary);
  color: white;
}

.item-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.del-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  opacity: 0.5;
  padding: 0 4px;
}

.list-item.active .del-btn {
  color: white;
}

.edit-input {
  flex: 1;
  border: 1px solid var(--primary);
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  background: var(--bg-card);
  color: var(--text);
}

.list-item.active .edit-input {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-color: rgba(255, 255, 255, 0.5);
}

.list-item.active .edit-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}
</style>
