import type { ButtonClickHandler } from './types'
import './stylesheets/App.css'

import chatService from './services/chatService'
import ChatWindow from './components/chatWindow'
import PageHeader from './components/PageHeader'

function App() {

  const handleClick: ButtonClickHandler = (e) => {
    e.preventDefault()
    chatService.getPing().then(data => {
      console.log(data)
    })
  }

  return (
    <div>
      <PageHeader />
      <ChatWindow />
    </div>
  )
}

export default App
