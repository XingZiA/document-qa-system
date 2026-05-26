import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Document } from '@/types'
import { listDocuments, uploadDocument, deleteDocument as delDoc } from '@/api/documents'

export const useDocumentStore = defineStore('document', () => {
  const documents = ref<Document[]>([])
  const uploading = ref(false)

  async function fetchDocuments() {
    documents.value = await listDocuments()
  }

  async function upload(file: File) {
    uploading.value = true
    try {
      const doc = await uploadDocument(file)
      documents.value.unshift({
        id: doc.id,
        filename: doc.filename,
        file_type: doc.file_type,
        chunk_count: 0,
        status: doc.status,
        created_at: new Date().toISOString(),
      })
      return doc
    } finally {
      uploading.value = false
    }
  }

  async function remove(id: number) {
    await delDoc(id)
    documents.value = documents.value.filter((d) => d.id !== id)
  }

  return { documents, uploading, fetchDocuments, upload, remove }
})
