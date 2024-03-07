import React, { useContext, useState } from "react";
import { useNavigate } from 'react-router-dom';
import Header from "./components/utils/Header";
import { ThemeProvider } from '@mui/material/styles';
import Theme from "./components/utils/Theme"
import { UserContext } from "./context/UserContext";
import ErrorMessage from "./components/admin_panel/ErrorMessage";
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, seterrorMessage] = useState("");
    const [, setToken] = useContext(UserContext);
    const navigate = useNavigate();

  const submitLogin = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, password: password }),
    };

    const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, requestOptions);
    const data = await response.json();
    if (!response.ok) {
      seterrorMessage(data.detail);
    } else {
      setToken(data.access_token);
      navigate("/upload");
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
                <Container component="main" maxWidth="xs">
                    <CssBaseline />
                    <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                    >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit}  noValidate sx={{ mt: 1 }}>
                        <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        className="input"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        autoComplete="username"
                        autoFocus
                        />
                        <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        className="input"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        autoComplete="current-password"
                        />
                        <ErrorMessage message={errorMessage} />
                        <br />
                        <Button
                        className="button is-primary"
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                        >
                        Sign In
                        </Button>
                    </Box>
                    </Box>
                </Container>
            </ThemeProvider>
        </React.StrictMode>
    );
    };

export default Login;