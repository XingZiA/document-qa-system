export interface Document {
  id: number
  filename: string
  file_type: string
  chunk_count: number
  status: string
  created_at: string
}

export interface Conversation {
  id: number
  title: string
  created_at: string
  updated_at: string
}

export interface Message {
  id: number
  conversation_id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface UploadResponse {
  id: number
  filename: string
  file_type: string
  status: string
  message: string
}

export interface ChatRequest {
  query: string
}

export interface SSEEvent {
  type: 'start' | 'token' | 'done'
  content?: string
  context_length?: number
}
