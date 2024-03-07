// TODO: Logout in proper place
import React, { useContext } from "react";
import { Button, ButtonGroup } from '@mui/material';
import { UserContext } from "./UserContext";
import { Link } from 'react-router-dom';


// import { AppBar, Box, Toolbar, Button } from '@mui/material';
const Logout = () => {
  const [, setToken] = useContext(UserContext);

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <ButtonGroup variant="contained" aria-label="Basic button group">
      <Button variant="contained" color="success" as={Link} to="/upload" style={{ textDecoration: 'none' }}>
        ADMIN PANEL
      </Button>
      <Button variant="contained" color="warning" onClick={handleLogout} as={Link} to="/" style={{ textDecoration: 'none' }}>
        LOGOUT
      </Button>
    </ButtonGroup>

  )
;
  
  ;
};

export default Logout;