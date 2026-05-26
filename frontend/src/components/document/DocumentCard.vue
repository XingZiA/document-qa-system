<script setup lang="ts">
import { useDocumentStore } from '@/stores/document'

const docStore = useDocumentStore()

async function handleRemove(id: number) {
  await docStore.remove(id)
}
</script>

<template>
  <div
    v-if="docStore.documents.length === 0"
    class="empty-docs"
  >
    暂无文档，点击 + 上传
  </div>
  <div
    v-for="doc in docStore.documents"
    :key="doc.id"
    class="doc-item"
  >
    <span class="doc-icon">
      {{ doc.file_type === 'pdf' ? '&#128196;' : doc.file_type === 'docx' ? '&#128220;' : '&#128462;' }}
    </span>
    <span class="doc-name">{{ doc.filename }}</span>
    <span
      class="doc-status"
      :class="doc.status"
    >{{ doc.status === 'ready' ? '✓' : '...' }}</span>
    <button
      class="doc-del"
      @click="handleRemove(doc.id)"
    >
      ×
    </button>
  </div>
</template>

<style scoped>
.doc-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 12px;
}

.doc-item:hover {
  background: rgba(0,0,0,0.04);
}

.doc-icon {
  font-size: 14px;
}

.doc-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.doc-status {
  font-size: 11px;
}

.doc-status.ready {
  color: #22c55e;
}

.doc-status.processing {
  color: #f59e0b;
}

.doc-del {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  opacity: 0.3;
}

.empty-docs {
  font-size: 12px;
  color: var(--text-secondary);
  padding: 8px;
  text-align: center;
}
</style>
