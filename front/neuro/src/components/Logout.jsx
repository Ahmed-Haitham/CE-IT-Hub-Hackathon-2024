// TODO: Logout in proper place
import React, { useContext } from "react";
import { AppBar, Box, Toolbar, Button } from '@mui/material';
import { UserContext } from "../context/UserContext";

const Logout = ({ title }) => {
  const [token, setToken] = useContext(UserContext);

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <div className="has-text-centered m-6">
      <h1 className="title">{title}</h1>
      {token && (
        <Button variant="contained" color="ochre" onClick={handleLogout} style={{ textDecoration: 'none' }}>
            LOGOUT
        </Button>
      )}
    </div>
  );
};

export default Logout;