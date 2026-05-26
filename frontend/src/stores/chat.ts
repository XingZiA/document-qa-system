import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Message } from '@/types'
import { getMessages } from '@/api/conversations'
import { streamChat } from '@/api/chat'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const streamingContent = ref('')
  const isStreaming = ref(false)
  const error = ref('')
  let abortController: AbortController | null = null

  async function loadMessages(convId: number) {
    messages.value = await getMessages(convId)
  }

  function startStream(convId: number, query: string) {
    isStreaming.value = true
    streamingContent.value = ''
    error.value = ''

    messages.value.push({
      id: Date.now(),
      conversation_id: convId,
      role: 'user',
      content: query,
      created_at: new Date().toISOString(),
    })

    abortController = streamChat(
      convId,
      query,
      (token) => {
        streamingContent.value += token
      },
      () => {
        messages.value.push({
          id: Date.now() + 1,
          conversation_id: convId,
          role: 'assistant',
          content: streamingContent.value,
          created_at: new Date().toISOString(),
        })
        streamingContent.value = ''
        isStreaming.value = false
      },
      (err) => {
        error.value = err
        isStreaming.value = false
      }
    )
  }

  function stopStream() {
    abortController?.abort()
    isStreaming.value = false
  }

  function clear() {
    messages.value = []
    streamingContent.value = ''
    error.value = ''
  }

  return { messages, streamingContent, isStreaming, error, loadMessages, startStream, stopStream, clear }
})
