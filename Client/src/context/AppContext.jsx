import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { dummyUserData, dummyChats } from "../assets/assets";

const AppContext = createContext()

export const AppContextProvider = ({ children }) => {

    const navigate = useNavigate()
    const [user, setUser] = useState(null);
    const [chats, setChats] = useState([]);
    const [loading, setLoading] = useState(false);
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");


    const fetchUser = async () => {
        setLoading(true)
        // Simulate auth + data fetch
        await new Promise(resolve => setTimeout(resolve, 500))
        setUser(dummyUserData)
        await fetchUsersChats()
        setLoading(false)
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

    const value = {
        navigate, user, setUser, fetchUser, chats, setChats,
        theme, setTheme, toggleTheme, fetchUsersChats, loading, setLoading
    }

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    )
}

export const useAppContext = () => useContext(AppContext)