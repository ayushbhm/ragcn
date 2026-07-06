import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000'
})

export const createSession = async () => {
  const res = await api.get('/session')
  return res.data.session_id
}

export const ingestPdf = async (formData) => {
  const res = await api.post('/ingest', formData)
  return res.data
}

export const askQuestion = async (sessionId, question, history) => {
  const res = await api.post('/ask', {
    session_id: sessionId,
    question,
    history
  })

  return res.data.answer
}