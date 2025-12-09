import React, { useEffect, useRef, useState } from 'react'

const CursorGlow = () => {
  const glowRef = useRef(null)
  const [isHovering, setIsHovering] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (glowRef.current) {
        // Position the glow circle at cursor
        glowRef.current.style.left = `${e.clientX - 15}px`
        glowRef.current.style.top = `${e.clientY - 15}px`
      }

      // Create trail effect occasionally
      if (Math.random() > 0.7) {
        createTrail(e.clientX, e.clientY)
      }
    }

    const handleMouseEnter = () => {
      if (glowRef.current) {
        glowRef.current.classList.add('active')
      }
    }

    const handleMouseLeave = () => {
      if (glowRef.current) {
        glowRef.current.classList.remove('active')
      }
    }

    const handleElementHover = (e) => {
      const target = e.target
      const isInteractive =
        target.tagName === 'BUTTON' ||
        target.tagName === 'A' ||
        target.getAttribute('role') === 'button' ||
        target.closest('button') ||
        target.closest('a') ||
        target.closest('[role="button"]')

      if (isInteractive) {
        setIsHovering(true)
        if (glowRef.current) {
          glowRef.current.classList.add('hover')
        }
      }
    }

    const handleElementLeave = (e) => {
      const target = e.target
      const isInteractive =
        target.tagName === 'BUTTON' ||
        target.tagName === 'A' ||
        target.getAttribute('role') === 'button' ||
        target.closest('button') ||
        target.closest('a') ||
        target.closest('[role="button"]')

      if (isInteractive) {
        setIsHovering(false)
        if (glowRef.current) {
          glowRef.current.classList.remove('hover')
        }
      }
    }

    // Check dark mode
    const updateDarkMode = () => {
      const isDark = document.documentElement.classList.contains('dark')
      setIsDarkMode(isDark)
      if (glowRef.current) {
        if (isDark) {
          glowRef.current.classList.add('dark')
        } else {
          glowRef.current.classList.remove('dark')
        }
      }
    }

    // Observer for dark mode changes
    const observer = new MutationObserver(updateDarkMode)
    observer.observe(document.documentElement, { attributes: true })

    // Initial dark mode check
    updateDarkMode()

    // Event listeners
    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseenter', handleMouseEnter)
    document.addEventListener('mouseleave', handleMouseLeave)
    document.addEventListener('mouseover', handleElementHover)
    document.addEventListener('mouseout', handleElementLeave)

    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseenter', handleMouseEnter)
      document.removeEventListener('mouseleave', handleMouseLeave)
      document.removeEventListener('mouseover', handleElementHover)
      document.removeEventListener('mouseout', handleElementLeave)
      observer.disconnect()
    }
  }, [])

  const createTrail = (x, y) => {
    const trail = document.createElement('div')
    trail.className = 'cursor-trail'
    trail.style.left = `${x - 4}px`
    trail.style.top = `${y - 4}px`
    document.body.appendChild(trail)

    setTimeout(() => trail.remove(), 800)
  }

  return (
    <div
      ref={glowRef}
      className='cursor-glow'
      style={{
        pointerEvents: 'none'
      }}
    />
  )
}

export default CursorGlow
