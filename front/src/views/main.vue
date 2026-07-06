<template>
  <div>

    <input type="file" accept=".pdf" @change="handleFileChange">

    <button @click="handleIngest">
      Upload PDF
    </button>

    <p v-if="status">{{ status }}</p>

    <input
      v-model="question"
      type="text"
      placeholder="Ask something about your PDF..."
      @keyup.enter="handleAsk"
    >

    <button
      @click="handleAsk"
      :disabled="!ingested || loading"
    >
      {{ loading ? "Thinking..." : "Ask" }}
    </button>

    <hr>

    <div
      v-for="(msg, i) in messages"
      :key="i"
      style="margin-bottom:20px;"
    >
      <p><strong>👤 You</strong></p>
      <p>{{ msg.q }}</p>

      <p><strong>🤖 Assistant</strong></p>
      <p>{{ msg.a }}</p>

      <hr>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { createSession, ingestPdf, askQuestion } from "../api.js"

const question = ref("")
const messages = ref([])

const ingested = ref(false)
const loading = ref(false)

const status = ref("")

const file = ref(null)
const sessionId = ref(null)

const handleFileChange = (e) => {
  file.value = e.target.files[0]
}

const handleIngest = async () => {

  status.value = "Uploading PDF..."

  const formData = new FormData()
  formData.append("file", file.value)
  formData.append("session_id", sessionId.value)

  await ingestPdf(formData)

  ingested.value = true
  status.value = "✅ PDF Ready"
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
  console.log("History being sent:");
 console.log(history);

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