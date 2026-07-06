<template>
  <div class="app">
    <header class="header">
      <h1>PDF Q&A</h1>
    </header>

    <section class="upload-row">
      <input type="file" accept=".pdf" @change="handleFileChange">
      <button class="btn" @click="handleIngest" :disabled="!file">
        Upload PDF
      </button>
      <span v-if="status" class="status">{{ status }}</span>
    </section>

    <section class="chat">
      <div v-if="messages.length === 0" class="empty">
        No messages yet. Upload a PDF and ask a question.
      </div>

      <div v-for="(msg, i) in messages" :key="i" class="message-pair">
        <div class="bubble user">
          <span class="label">You</span>
          <p>{{ msg.q }}</p>
        </div>
        <div class="bubble assistant">
          <span class="label">Assistant</span>
          <div class="markdown" v-html="renderMarkdown(msg.a)"></div>
        </div>
      </div>
    </section>

    <section class="ask-row">
      <input
        v-model="question"
        type="text"
        placeholder="Ask something about your PDF..."
        @keyup.enter="handleAsk"
      >
      <button
        class="btn"
        @click="handleAsk"
        :disabled="!ingested || loading || !question.trim()"
      >
        {{ loading ? "Thinking..." : "Ask" }}
      </button>
    </section>

    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { marked } from "marked"
import { createSession, ingestPdf, askQuestion } from "../api.js"

const question = ref("")
const messages = ref([])

const ingested = ref(false)
const loading = ref(false)

const status = ref("")
const errorMsg = ref("")

const file = ref(null)
const sessionId = ref(null)

marked.setOptions({ breaks: true })

const renderMarkdown = (text) => marked.parse(text || "")

const handleFileChange = (e) => {
  file.value = e.target.files[0]
  status.value = ""
  errorMsg.value = ""
}

const handleIngest = async () => {
  if (!file.value) {
    errorMsg.value = "Please choose a PDF file first."
    return
  }

  errorMsg.value = ""
  status.value = "Uploading PDF..."

  const formData = new FormData()
  formData.append("file", file.value)
  formData.append("session_id", sessionId.value)

  await ingestPdf(formData)

  ingested.value = true
  status.value = "PDF Ready"
}

const handleAsk = async () => {
  if (!question.value.trim()) return

  const q = question.value
  question.value = ""

  loading.value = true

  let history = ""

  for (const msg of messages.value) {
    history += `User: ${msg.q}\n`
    history += `Assistant: ${msg.a}\n\n`
  }

  const ans = await askQuestion(
    sessionId.value,
    q,
    history
  )

  messages.value.push({
    q,
    a: ans
  })

  loading.value = false
}

onMounted(async () => {
  sessionId.value = await createSession()
})
</script>

<style scoped>
.app {
  max-width: 720px;
  margin: 0 auto;
  padding: 24px 16px 40px;
  font-family: system-ui, sans-serif;
  background: #fff;
  color: #1a1a1a;
  min-height: 100vh;
}

.header h1 {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 20px;
  color: #1a1a1a;
}

.upload-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.status {
  font-size: 14px;
  color: #42b883;
}

.chat {
  background: #fafafa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  min-height: 240px;
  max-height: 460px;
  overflow-y: auto;
  padding: 16px;
  margin-bottom: 20px;
}

.empty {
  color: #999;
  font-size: 14px;
}

.message-pair {
  margin-bottom: 18px;
}

.bubble {
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 8px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-left: 3px solid #1a1a1a;
}

.bubble.assistant {
  border-left: 3px solid #42b883;
}

.label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #888;
}

.bubble.assistant .label {
  color: #42b883;
}

.bubble p {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
}

/* rendered markdown from assistant answers */
.markdown {
  font-size: 14px;
  line-height: 1.6;
}

.markdown :deep(p) {
  margin: 0 0 8px;
}

.markdown :deep(ul),
.markdown :deep(ol) {
  margin: 0 0 8px;
  padding-left: 20px;
}

.markdown :deep(li) {
  margin-bottom: 4px;
}

.markdown :deep(strong) {
  font-weight: 700;
}

.markdown :deep(code) {
  background: #f0f0f0;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 13px;
}

.markdown :deep(pre) {
  background: #f0f0f0;
  padding: 10px;
  border-radius: 6px;
  overflow-x: auto;
}

.ask-row {
  display: flex;
  gap: 10px;
}

input[type="text"] {
  flex: 1;
  padding: 10px 12px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  color: #1a1a1a;
}

input[type="text"]:focus {
  outline: none;
  border-color: #42b883;
}

.btn {
  padding: 10px 18px;
  background: #42b883;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn:disabled {
  background: #d5d5d5;
  color: #888;
  cursor: not-allowed;
}

.error {
  color: #c0392b;
  font-size: 13px;
  margin-top: 10px;
}
</style>