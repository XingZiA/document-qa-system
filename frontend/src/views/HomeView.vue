<script setup lang="ts">
import ChatWindow from '@/components/chat/ChatWindow.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
</script>

<template>
  <div class="home">
    <ChatWindow />
    <ChatInput />
  </div>
</template>

<style scoped>
.home {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
