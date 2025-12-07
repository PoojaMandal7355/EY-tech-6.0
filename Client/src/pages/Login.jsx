import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppContext } from '../context/AppContext'
import { loginUser as apiLogin, registerUser as apiRegister, requestPasswordReset } from '../utils/authApi'

const Login = () => {

  const [state, setState] = useState("login") // login | register | forgot
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [info, setInfo] = useState("")
  const [loading, setLoading] = useState(false)

  const navigate = useNavigate()
  const { loginUser } = useAppContext()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setInfo("")
    setLoading(true)
    
    try {
      if (state === "forgot") {
        if (!email) {
          setError("Please enter your email to reset password")
          setLoading(false)
          return
        }
        await requestPasswordReset(email)
        setInfo("If this email is registered, a password reset link has been sent.")
        setState("login")
      } else if (state === "register") {
        // Register new user
        if (password.length < 8) {
          setError("Password must be at least 8 characters")
          setLoading(false)
          return
        }
        
        const userData = await apiRegister(email, fullName, password)
        
        // Auto-login after registration
        await apiLogin(email, password)
        loginUser(userData)
        navigate('/loading')
      } else {
        // Login existing user
        await apiLogin(email, password)
        
        // Fetch user data from context
        const userData = {
          email,
          full_name: fullName
        }
        loginUser(userData)
        navigate('/loading')
      }
    } catch (err) {
      // Show a clearer message for bad credentials or generic failure
      const msg = err?.message?.toLowerCase() || ""
      if (state === "forgot") {
        setError("Unable to send reset email right now. Please try again.")
      } else if (msg.includes("invalid") || msg.includes("unauthorized")) {
        setError("Incorrect email or password. Please try again.")
      } else {
        setError(err.message || "Something went wrong. Please try again.")
      }
      console.error("Auth error:", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 m-auto items-start p-8 py-12 w-80 sm:w-[352px] text-gray-500 rounded-lg shadow-xl border border-gray-200 bg-white">
      <p className="text-2xl font-medium m-auto">
        <span className="text-emerald-600">User</span> {state === "login" ? "Login" : state === "register" ? "Sign Up" : "Forgot Password"}
      </p>
      {info && (
        <div className="w-full p-3 rounded bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm">
          {info}
        </div>
      )}
      {error && (
        <div className="w-full p-3 rounded bg-red-100 border border-red-300 text-red-700 text-sm">
          {error}
        </div>
      )}
      {state === "register" && (
        <div className="w-full">
          <p>Full Name</p>
          <input onChange={(e) => setFullName(e.target.value)} value={fullName} placeholder="type here" className="border border-gray-200 rounded w-full p-2 mt-1 outline-emerald-500" type="text" required />
        </div>
      )}
      <div className="w-full">
        <p>Email</p>
        <input onChange={(e) => setEmail(e.target.value)} value={email} placeholder="type here" className="border border-gray-200 rounded w-full p-2 mt-1 outline-emerald-500" type="email" required />
      </div>
      {state !== "forgot" && (
        <div className="w-full ">
          <p>Password</p>
          <input onChange={(e) => setPassword(e.target.value)} value={password} placeholder="type here" className="border border-gray-200 rounded w-full p-2 mt-1 outline-emerald-500" type="password" required />
          {state === "register" && (
            <p className="text-xs text-gray-400 mt-1">Minimum 8 characters required</p>
          )}
          {state === "login" && (
            <p className="text-xs text-emerald-600 mt-2 cursor-pointer" onClick={() => { setState("forgot"); setError(""); setInfo(""); }}>Forgot password?</p>
          )}
        </div>
      )}

      {state === "register" && (
        <p>
          Already have account? <span onClick={() => { setState("login"); setError(""); setInfo(""); }} className="text-emerald-600 cursor-pointer">click here</span>
        </p>
      )}
      {state === "login" && (
        <p>
          Create an account? <span onClick={() => { setState("register"); setError(""); setInfo(""); }} className="text-emerald-600 cursor-pointer">click here</span>
        </p>
      )}
      {state === "forgot" && (
        <p>
          Remembered your password? <span onClick={() => { setState("login"); setError(""); setInfo(""); }} className="text-emerald-600 cursor-pointer">Back to login</span>
        </p>
      )}

      <button type="submit" disabled={loading} className="bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all text-white w-full py-2 rounded-md cursor-pointer shadow-md shadow-emerald-400/40">
        {loading ? "Loading..." : state === "register" ? "Create Account" : state === "forgot" ? "Send reset link" : "Login"}
      </button>
    </form>
  )
}

export default Login
