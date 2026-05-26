<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import TypewriterText from './TypewriterText.vue'

const props = defineProps<{
  role: 'user' | 'assistant'
  content: string
  isStreaming: boolean
}>()

const renderedHtml = computed(() => {
  return marked.parse(props.content, { breaks: true }) as string
})
</script>

<template>
  <div
    class="message"
    :class="role"
  >
    <div class="avatar">
      {{ role === 'user' ? 'U' : 'AI' }}
    </div>
    <div class="bubble">
      <TypewriterText
        v-if="isStreaming"
        :text="content"
        :enabled="true"
        :speed="20"
      />
      <div
        v-else
        class="markdown-body"
        v-html="renderedHtml"
      />
    </div>
  </div>
</template>

<style scoped>
.message {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}

.user .avatar {
  background: var(--primary);
  color: white;
}

.assistant .avatar {
  background: #e0e7ff;
  color: var(--primary);
}

.bubble {
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 75%;
  font-size: 14px;
  line-height: 1.6;
}

.user .bubble {
  background: var(--primary);
  color: white;
  border-bottom-right-radius: 4px;
}

.assistant .bubble {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-bottom-left-radius: 4px;
}

/* Markdown 渲染样式 */
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  font-weight: 700;
  margin-bottom: 8px;
  margin-top: 12px;
}

.markdown-body :deep(h1) { font-size: 1.4em; }
.markdown-body :deep(h2) { font-size: 1.2em; }
.markdown-body :deep(h3) { font-size: 1.05em; }

.markdown-body :deep(p) {
  margin-bottom: 8px;
}

.markdown-body :deep(strong) {
  font-weight: 700;
  color: var(--primary);
}

.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid var(--border);
  margin: 12px 0;
}

.markdown-body :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
}

.markdown-body :deep(code) {
  font-family: 'Fira Code', monospace;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 20px;
  margin-bottom: 8px;
}

.markdown-body :deep(li) {
  margin-bottom: 4px;
}
</style>
