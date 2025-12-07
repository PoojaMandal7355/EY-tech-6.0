import React from 'react'
import { useAppContext } from '../context/AppContext'
import { assets } from '../assets/assets'
import { useNavigate, useLocation } from 'react-router-dom'

const NavBar = () => {
  const { user, theme, toggleTheme } = useAppContext()
  const navigate = useNavigate()
  const location = useLocation()
  const isHome = location && (location.pathname === '/' || location.pathname === '')
  const showLogo = !(user && !isHome)

  return (
    <header className='sticky top-0 z-50 w-full border-b border-gray-200/30 dark:border-white/10 bg-white/30 dark:bg-white/5 backdrop-blur-lg shadow-lg shadow-emerald-500/20'>
      <div className='max-w-7xl mx-auto px-5 py-3 flex items-center justify-between'>

        {/* LEFT SIDE — Logo + Nav */}
        <div className='flex items-center gap-6 text-base md:text-lg font-medium text-gray-700 dark:text-gray-200'>

          {/* Logo LEFTMOST */}
          {showLogo && (
            <img
              src={theme === 'dark' ? assets.logo_full : assets.logo_full_dark}
              alt='logo'
              className='h-12 w-auto object-contain'
            />
          )}

          {/* Nav links */}
          <nav className='hidden md:flex items-center gap-6 ml-2'>
            <a onClick={() => {
              navigate('/')
              setTimeout(() => {
                window.scrollTo({ top: 0, behavior: 'smooth' })
              }, 100)
            }} className='hover:underline cursor-pointer'>Home</a>
            <a onClick={() => {
              navigate('/')
              setTimeout(() => {
                document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
              }, 100)
            }} className='hover:underline cursor-pointer'>Features</a>
            <a className='hover:underline cursor-pointer'>Pricing</a>
            <a className='hover:underline cursor-pointer'>Docs</a>
          </nav>
        </div>

        {/* RIGHT SIDE — Actions */}
        <div className='flex items-center gap-4 text-base md:text-lg font-medium'>
          {/* Theme Toggle */}
          <button 
            onClick={toggleTheme}
            className='p-1.5 rounded-md bg-gradient-to-r from-[#10b981] to-[#34d399] hover:shadow-lg hover:shadow-emerald-500/50 transition-all duration-300 hover:scale-105'
            aria-label='Toggle theme'
          >
            <img 
              src={assets.theme_icon} 
              alt='theme' 
              className='w-4 h-4 brightness-0 invert'
            />
          </button>

          <button onClick={() => navigate('/loading')} className='hidden md:inline-block px-4 py-1.5 rounded-md bg-gradient-to-r from-[#10b981] to-[#34d399] text-white text-sm font-semibold transition-all duration-300 hover:scale-102 hover:shadow-lg hover:shadow-emerald-500/50'>
            Get Started
          </button>

          {user ? (
            <div className='flex items-center gap-2 text-sm'>
              <img src={assets.user_icon} className='w-7 h-7 rounded-full' alt='user' />
              <span className='dark:text-white font-semibold'>{user.name}</span>
            </div>
          ) : (
            <button onClick={() => navigate('/loading')} className='px-3 py-1.5 rounded-md border border-[#10b981] text-[#10b981] dark:text-[#10b981] text-sm font-semibold hover:bg-[#10b981] hover:text-white transition-colors'>
              Sign in
            </button>
          )}
        </div>
      </div>
    </header>
  )
}

export default NavBar
