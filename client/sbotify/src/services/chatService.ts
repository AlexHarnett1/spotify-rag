import axios from 'axios'

// const baseUrl = '/api'

const getPing = () => {
  const request = axios.get(`/api/ping`)
  return request.then(response => response.data)
}

const getBotReply = (message: string) => {
  const request = axios.post('/api/chat', { userMessage: message })
  return request.then(response => response.data)
}

export default {
  getPing, getBotReply
}