import React, { useEffect } from 'react'
import { useAppContext } from '../context/AppContext'
import { useState } from 'react'
import { assets } from '../assets/assets'
import Message from './Message'

const ChatBox = () => {

  const { chats, theme } = useAppContext()
  const [messages, setMessages] = useState([])
  const [Loading, setLoading] = useState(false)

  const [prompt, setPrompt] = useState('')
  const [mode, setMode] = useState('text')
  const [isPublished, setIsPublished] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
  }


  useEffect(() => {
    if (chats && chats.length > 0) {
      setMessages(chats[0].messages || [])
    } else {
      setMessages([])
    }
  }, [chats])



  return (
    <div className='flex-1 flex flex-col justify-between p-5 md:p-10 max-md:pt-20 2xl:pr-40 h-full overflow-hidden bg-gray-50 dark:bg-transparent'>
      {/* chat messages */}
      <div className='flex-1 mb-5 overflow-y-auto'>
        {messages.length === 0 && (
          <div className='h-full flex flex-col items-center justify-center gap-2 text-primary'>
            <img src={theme === 'dark' ? assets.logo_full : assets.logo_full_dark} alt="no-messages" className='w-full max-w-56 sm:max-w-68 pointer-events-none'/>
            <p className='mt-5 text-4xl sm:text-6xl text-centre text-grey-400 dark:text-white'>Start Your Research</p>
            <p className='text-sm sm:text-base text-gray-500 dark:text-gray-400 max-w-md text-center'>Ask questions, analyze data, and discover insights. Type your query below to begin.</p>
          </div>
        )}

        {messages.map((message, index) => <Message key={index} message={message} />)}
      {/* There dots loading */}
      {
        Loading && <div className='loader flex items-center gap-1.5'>
          <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
          <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
          <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
        </div>
      }
      
      </div>
      {/* Prompt Input Box */}
      <form className='bg-green-100 dark:bg-green-900/30 border border-green-300 dark:border-green-700/50 rounded-full w-full max-w-2xl p-3 pl-4 mx-auto flex gap-4 items-center shrink-0' onSubmit={onSubmit}>
        {/* <select className='text-sm pl-3 pr-2 outline-none'>
          <option value="text">Text</option>
        </select> */}
        <textarea placeholder='Type your prompt here...' className='flex-1 w-full text-sm outline-none resize-none bg-transparent max-h-32 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-gray-400 dark:scrollbar-thumb-gray-600 py-2 text-black dark:text-white placeholder-gray-600 dark:placeholder-gray-400' required rows="1" onInput={(e) => {
          e.target.style.height = 'auto';
          e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px';
        }}/>
        <button disabled={Loading} type="submit">
          <img src={Loading ? assets.stop_icon : assets.send_icon} className='w-8 cursor-pointer shrink-0' alt="" />
        </button>
      </form>
    </div>
  )
}

export default ChatBox
