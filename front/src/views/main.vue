<template>
  <div>
    <p>Session: {{ sessionId }}</p>
  </div>


<input type="file" accept=".pdf" @change="handleFileChange">

  <button @click="handleIngest"> Add Video</button>



<input v-model="question" type="text" placeholder="Ask some questions">
<button @click="handleAsk"> Ask</button>
<p v-if="answer">{{ answer }}</p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createSession, ingestPdf, askQuestion } from '../api.js'


const question = ref('')
const answer = ref('')

const file = ref(null)


const sessionId = ref(null)
const handleIngest = async () => {
  

  const formData = new FormData()
  formData.append('file' , file.value)
  formData.append('session_id', sessionId.value
  )

  await ingestPdf(formData)
}

const handleFileChange = (e) => {
  file.value = e.target.files[0]
}

const handleAsk = async () => {
  answer.value = await askQuestion(sessionId.value, question.value)
}

onMounted(async () => {
  sessionId.value = await createSession()
  console.log('Session ID:', sessionId.value)
})
</script>