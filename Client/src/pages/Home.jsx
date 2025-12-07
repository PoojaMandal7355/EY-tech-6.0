import React from 'react'
import NavBar from '../components/NavBar'
import Hero from '../components/Hero'
import Features from '../components/Features'

const Home = () => {
  return (
    <div className='flex flex-col bg-gradient-to-b from-[#d1fae5] via-[#a7f3d0] to-[#f0fdf4] dark:bg-gradient-to-b dark:from-[#242124] dark:to-[#000000]'>
      <NavBar />
      <Hero />
      <Features />
    </div>
  )
}

export default Home
