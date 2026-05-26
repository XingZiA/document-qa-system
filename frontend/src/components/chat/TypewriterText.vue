<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue'
import { marked } from 'marked'

marked.setOptions({ breaks: true, gfm: true })

const props = withDefaults(defineProps<{
  text: string
  enabled: boolean
  speed?: number
}>(), {
  speed: 20,
})

const displayed = ref('')
let timer: ReturnType<typeof setInterval> | null = null
let typedLen = 0

watch(() => props.text, (val) => {
  if (!props.enabled) {
    displayed.value = val
    return
  }
  if (val.startsWith(displayed.value)) {
    typedLen = displayed.value.length
  } else {
    displayed.value = ''
    typedLen = 0
  }
  startTyping(val)
})

function startTyping(fullText: string) {
  if (timer) clearInterval(timer)
  timer = setInterval(() => {
    if (typedLen < fullText.length) {
      const chunk = fullText.slice(typedLen, typedLen + props.speed)
      displayed.value += chunk
      typedLen += props.speed
    } else {
      if (timer) clearInterval(timer)
    }
  }, 30)
}

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div
    v-if="enabled"
    class="streaming-text"
  >
    {{ displayed }}
  </div>
  <div
    v-else
    class="markdown-body"
    v-html="marked(text)"
  />
</template>

<style scoped>
.streaming-text {
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 14px;
}
</style>
