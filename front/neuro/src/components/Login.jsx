import React, { useState, useContext } from "react";
import Header from "../Header";

import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";
import { ThemeProvider } from '@mui/material/styles';
import Theme from "../Theme"

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, seterrorMessage] = useState("");
    // const [, setToken] = useContext(UserContext);

  const submitLogin = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, hashed_password: password }),
    };

    const response = await fetch("/api/login", requestOptions);
    // const data = await response.json();
    const data = JSON.stringify({ access_token: 'asdad', detail: 'dadsa'})
    if (!response.ok) {
      seterrorMessage(data.detail);
    } else {
    //   setToken(data.access_token);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitLogin();
  };

    return (
        <React.StrictMode>
            <ThemeProvider theme={Theme}>
                <Header />
                <div className="column">
                {/* <form className="box" onSubmit={handleSubmit}> */}
                <form className="box">
                    <h1 className="title has-text-centered">Login</h1>
                    <div className="field">
                    <label className="label">Username</label>
                    <div className="control">
                        <input
                        type="username"
                        placeholder="Enter username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="input"
                        required
                        />
                    </div>
                    </div>
                    <div className="field">
                    <label className="label">Password</label>
                    <div className="control">
                        <input
                        type="password"
                        placeholder="Enter password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="input"
                        required
                        />
                    </div>
                    </div>
                    <ErrorMessage message={errorMessage} />
                    <br />
                    <button className="button is-primary" type="submit">
                    Login
                    </button>
                </form>
                </div>
            </ThemeProvider>
        </React.StrictMode>
    );
    };

export default Login;