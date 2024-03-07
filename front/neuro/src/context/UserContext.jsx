import React, { createContext, useEffect, useState } from "react";

export const UserContext = createContext()

export const UserProvider = (props) => {
    const [token, setToken] = useState(localStorage.getItem("diseaseAppToken"));

    useEffect(() => {
        const fetchUser = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                }
            }
        }
    })
}