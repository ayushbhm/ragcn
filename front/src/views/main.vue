<template>
  <div>
    <p>Session: {{ sessionId }}</p>
  </div>


<input type="file" accept=".pdf" @change="handleFileChange">

  <button @click="handleIngest"> Add Video</button>



<input v-model="question" type="text" placeholder="Ask some questions">



<p v-if="answer">{{ answer }}</p>


<p v-if="status"> {{status}}</p>
<button @click="handleAsk" :disabled="!ingested"> Ask </button>


<div v-for="(msg, i) in messages" :key="i">
  <p><strong>You:</strong> {{ msg.q }}</p>
  <p><strong>Answer:</strong> {{ msg.a }}</p>
</div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createSession, ingestPdf, askQuestion } from '../api.js'


const question = ref('')
const answer = ref('')

const messages =ref([])
const ingested = ref(false)
const status = ref('')


const file = ref(null)


const sessionId = ref(null)
const handleIngest = async () => {

  status.value = 'Processing'

  

  const formData = new FormData()
  formData.append('file' , file.value)
  formData.append('session_id', sessionId.value
  )

  await ingestPdf(formData)
  ingested.value = true
  status.value= "ready"
}

const handleFileChange = (e) => {
  file.value = e.target.files[0]
}

const handleAsk = async () => {
  const q = question.value
  question.value = ''
  const ans = await askQuestion(sessionId.value,q)
  messages.value.push({q: q, a: ans})

 
  
}

onMounted(async () => {
  sessionId.value = await createSession()
  console.log('Session ID:', sessionId.value)
})
</script>