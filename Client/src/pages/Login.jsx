import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppContext } from '../context/AppContext'

const Login = () => {

  const [state, setState] = useState("login")
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const navigate = useNavigate()
  const { fetchUser } = useAppContext()

  const handleSubmit = async (e) => {
    e.preventDefault()
    fetchUser()
    navigate('/loading')
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 m-auto items-start p-8 py-12 w-80 sm:w-[352px] text-gray-500 rounded-lg shadow-xl border border-gray-200 bg-white">
      <p className="text-2xl font-medium m-auto">
        <span className="text-emerald-600">User</span> {state === "login" ? "Login" : "Sign Up"}
      </p>
      {state === "register" && (
        <div className="w-full">
          <p>Name</p>
          <input onChange={(e) => setName(e.target.value)} value={name} placeholder="type here" className="border border-gray-200 rounded w-full p-2 mt-1 outline-emerald-500" type="text" required />
        </div>
      )}
      <div className="w-full">
        <p>Email</p>
        <input onChange={(e) => setEmail(e.target.value)} value={email} placeholder="type here" className="border border-gray-200 rounded w-full p-2 mt-1 outline-emerald-500" type="email" required />
      </div>
      <div className="w-full ">
        <p>Password</p>
        <input onChange={(e) => setPassword(e.target.value)} value={password} placeholder="type here" className="border border-gray-200 rounded w-full p-2 mt-1 outline-emerald-500" type="password" required />
      </div>
      {state === "register" ? (
        <p>
          Already have account? <span onClick={() => setState("login")} className="text-emerald-600 cursor-pointer">click here</span>
        </p>
      ) : (
        <p>
          Create an account? <span onClick={() => setState("register")} className="text-emerald-600 cursor-pointer">click here</span>
        </p>
      )}
      <button type="submit" className="bg-gradient-to-r from-[#10b981] to-[#34d399] hover:brightness-110 transition-all text-white w-full py-2 rounded-md cursor-pointer shadow-md shadow-emerald-400/40">
        {state === "register" ? "Create Account" : "Login"}
      </button>
    </form>
  )
}

export default Login
