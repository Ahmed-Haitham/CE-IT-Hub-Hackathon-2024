import React from 'react';
import wum_logo from '../../assets/Logo_WUM.png';
import pg_logo from '../../assets/PGlogo.png';
import { AppBar, Box, Toolbar, Button } from '@mui/material';
import { Link } from 'react-router-dom'; 

const Header = () => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        {/* Logo (for home navigation) - top left */}
        
        <Box marginRight={4} as={Link} to="/">
        <img src={wum_logo} alt="Logo" style={{maxHeight: '50px', flexGrow: 1}} />
        <img src={pg_logo} alt="Logo" style={{maxHeight: '50px', flexGrow: 1}} />
        </Box>
        
        {/* Spacer */}
        <Box flexGrow={1} />

        {/* Admin log in button - top right */}
        <Box marginRight={4}>
        <Button variant="text" color="inherit">Learn More</Button>
        </Box>
        <Button variant="contained" color="ochre" as={Link} to="/login" style={{ textDecoration: 'none' }}>ADMIN LOG IN</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;