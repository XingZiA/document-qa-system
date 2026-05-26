import api from './index'
import type { Document, UploadResponse } from '@/types'

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post<UploadResponse>('/documents/upload', form)
  return data
}

export async function listDocuments(): Promise<Document[]> {
  const { data } = await api.get<Document[]>('/documents')
  return data
}

export async function deleteDocument(id: number): Promise<void> {
  await api.delete(`/documents/${id}`)
}
