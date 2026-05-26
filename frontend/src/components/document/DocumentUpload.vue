<script setup lang="ts">
import { ref } from 'vue'
import { useDocumentStore } from '@/stores/document'

const emit = defineEmits<{ close: [] }>()
const docStore = useDocumentStore()
const dragging = ref(false)
const error = ref('')
const success = ref('')

function onDragOver(e: DragEvent) {
  e.preventDefault()
  dragging.value = true
}

function onDragLeave() {
  dragging.value = false
}

async function onDrop(e: DragEvent) {
  e.preventDefault()
  dragging.value = false
  const file = e.dataTransfer?.files[0]
  if (file) await processFile(file)
}

async function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) await processFile(file)
}

async function processFile(file: File) {
  error.value = ''
  success.value = ''
  const allowed = ['pdf', 'docx', 'doc', 'txt', 'md', 'markdown']
  const ext = file.name.split('.').pop()?.toLowerCase() || ''
  if (!allowed.includes(ext)) {
    error.value = `不支持的文件类型: .${ext}`
    return
  }
  try {
    const result = await docStore.upload(file)
    success.value = result.message
    setTimeout(() => emit('close'), 1000)
  } catch (e: any) {
    error.value = e.response?.data?.detail || e.message
  }
}
</script>

<template>
  <div
    class="modal-overlay"
    @click.self="emit('close')"
  >
    <div class="modal">
      <h3>上传文档</h3>
      <div
        class="drop-zone"
        :class="{ dragging }"
        @dragover="onDragOver"
        @dragleave="onDragLeave"
        @drop="onDrop"
      >
        <p v-if="!docStore.uploading">
          拖拽文件到此处，或点击选择
        </p>
        <p v-else>
          上传中...
        </p>
        <input
          type="file"
          accept=".pdf,.docx,.doc,.txt,.md"
          @change="onFileChange"
        >
      </div>
      <p
        v-if="error"
        class="msg error"
      >
        {{ error }}
      </p>
      <p
        v-if="success"
        class="msg success"
      >
        {{ success }}
      </p>
      <button
        class="close-btn"
        @click="emit('close')"
      >
        关闭
      </button>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.modal h3 {
  font-size: 18px;
}

.drop-zone {
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
}

.drop-zone.dragging {
  border-color: var(--primary);
  background: #eef2ff;
}

.drop-zone input {
  display: block;
  margin: 8px auto 0;
  font-size: 13px;
}

.msg {
  font-size: 13px;
  text-align: center;
}

.msg.error {
  color: #ef4444;
}

.msg.success {
  color: #22c55e;
}

.close-btn {
  padding: 8px;
  background: var(--border);
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 14px;
}
</style>
