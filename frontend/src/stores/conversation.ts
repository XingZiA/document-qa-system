import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Conversation } from '@/types'
import {
  listConversations,
  createConversation,
  updateConversation,
  deleteConversation as delConv,
} from '@/api/conversations'

export const useConversationStore = defineStore('conversation', () => {
  const conversations = ref<Conversation[]>([])
  const activeId = ref<number | null>(null)

  async function fetchConversations() {
    conversations.value = await listConversations()
  }

  async function create(title = 'New Chat') {
    const conv = await createConversation(title)
    conversations.value.unshift(conv)
    activeId.value = conv.id
    return conv
  }

  async function remove(id: number) {
    await delConv(id)
    conversations.value = conversations.value.filter((c) => c.id !== id)
    if (activeId.value === id) {
      activeId.value = conversations.value[0]?.id || null
    }
  }

  function setActive(id: number) {
    activeId.value = id
  }

  async function rename(id: number, title: string) {
    const conv = await updateConversation(id, title)
    const target = conversations.value.find((c) => c.id === id)
    if (target) {
      target.title = conv.title
    }
  }

  function autoTitle(id: number, message: string) {
    const short = message.replace(/\s+/g, ' ').trim()
    const title = short.length > 20 ? short.slice(0, 20) + '...' : short
    return rename(id, title)
  }

  return { conversations, activeId, fetchConversations, create, remove, setActive, rename, autoTitle }
})
