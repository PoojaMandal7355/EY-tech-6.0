import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser, getAccessToken, logoutUser as logoutFromAuth } from "../utils/authApi";

const AppContext = createContext()

export const AppContextProvider = ({ children }) => {

    const navigate = useNavigate()
    const [user, setUser] = useState(null);
    const [chats, setChats] = useState([]);
    const [loading, setLoading] = useState(false);
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");


    const fetchUser = async () => {
        setLoading(true)
        const accessToken = getAccessToken()
        
        if (accessToken) {
            try {
                // Fetch user info from backend
                const userData = await getCurrentUser(accessToken)
                setUser(userData)
                localStorage.setItem("user", JSON.stringify(userData))
                await fetchUsersChats()
            } catch (error) {
                console.error("Failed to fetch user:", error)
                logoutFromAuth()
                setUser(null)
                navigate("/login")
            }
        } else {
            // No access token - user needs to login
            setUser(null)
        }
        setLoading(false)
    }

    const loginUser = (userData) => {
        // userData comes from backend, tokens are already stored by authApi
        setUser(userData)
        localStorage.setItem("user", JSON.stringify(userData))
    }

    const logoutUser = () => {
        setUser(null)
        setChats([])
        logoutFromAuth()
        navigate("/login")
    }

    const fetchUsersChats = async () => {
        // Simulate network latency for chat data
        await new Promise(resolve => setTimeout(resolve, 700))
        // Start with empty chats - fresh slate for new users
        setChats([])
    }
    const toggleTheme = () => {
        setTheme(prevTheme => prevTheme === "light" ? "dark" : "light")
    }

    useEffect(() => {
        if (theme === "dark") {
            document.documentElement.classList.add("dark")
        } else {
            document.documentElement.classList.remove("dark")
        }
        localStorage.setItem("theme", theme)
    }, [theme])

    useEffect(() => {
        if (!user) {
            setChats([])
        }
    }, [user])

    // Check for existing token on mount
    useEffect(() => {
        fetchUser()
    }, [])

    const value = {
        navigate, user, setUser, fetchUser, loginUser, logoutUser, chats, setChats,
        theme, setTheme, toggleTheme, fetchUsersChats, loading, setLoading
    }

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    )
}

export const useAppContext = () => useContext(AppContext)