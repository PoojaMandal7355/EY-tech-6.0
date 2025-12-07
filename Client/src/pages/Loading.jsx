import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppContext } from '../context/AppContext'

const Loading = () => {
  const navigate = useNavigate()
  const { loading, user, fetchUser } = useAppContext()
  const [minLoadingComplete, setMinLoadingComplete] = React.useState(false)

  useEffect(() => {
    // Always show minimum loading time
    const minTimer = setTimeout(() => {
      setMinLoadingComplete(true)
    }, 1200)

    // If user doesn't exist, trigger auth fetch
    if (!user && !loading) {
      fetchUser()
    }

    return () => clearTimeout(minTimer)
  }, [])

  useEffect(() => {
    // Only navigate after both loading finished AND minimum display time
    if (minLoadingComplete && !loading) {
      if (user) {
        navigate('/chat', { replace: true })
      } else {
        navigate('/login', { replace: true })
      }
    }
  }, [minLoadingComplete, loading, user, navigate])

  return (
    <div className='bg-linear-to-b from-[#189130] to-[#164518] backdrop-opacity-60 flex items-center justify-center h-screen w-screen text-white text-2xl'>
      <div className='w-10 h-10 rounded-full border-4 border-white border-t-transparent animate-spin'></div>
    </div>
  )
}

export default Loading
