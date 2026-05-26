import api from './index'
import type { Conversation, Message } from '@/types'

export async function createConversation(title = 'New Chat'): Promise<Conversation> {
  const { data } = await api.post<Conversation>('/conversations', { title })
  return data
}

export async function listConversations(): Promise<Conversation[]> {
  const { data } = await api.get<Conversation[]>('/conversations')
  return data
}

export async function getMessages(convId: number): Promise<Message[]> {
  const { data } = await api.get<Message[]>(`/conversations/${convId}/messages`)
  return data
}

export async function updateConversation(id: number, title: string): Promise<Conversation> {
  const { data } = await api.patch<Conversation>(`/conversations/${id}`, { title })
  return data
}

export async function deleteConversation(id: number): Promise<void> {
  await api.delete(`/conversations/${id}`)
}
