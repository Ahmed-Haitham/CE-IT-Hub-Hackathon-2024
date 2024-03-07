// TODO: Logout in proper place
import React, { useContext } from "react";
import { Button } from '@mui/material';
import { UserContext } from "./UserContext";

const Logout = () => {
  const [, setToken] = useContext(UserContext);

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <Button variant="contained" color="warning" onClick={handleLogout} style={{ textDecoration: 'none' }}>
        LOGOUT
    </Button>

  );
};

export default Logout;