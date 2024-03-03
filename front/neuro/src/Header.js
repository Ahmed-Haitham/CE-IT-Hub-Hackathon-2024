import React from 'react';
import wum_logo from './assets/Logo_WUM.png';
import pg_logo from './assets/PGlogo.png';
import { AppBar, Box, Toolbar, Button } from '@mui/material';

const Header = () => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        {/* Logo (for home navigation) - top left */}
        
        <Box marginRight={4}>
        <img src={wum_logo} alt="Logo" style={{maxHeight: '50px', flexGrow: 1}} />
        <img src={pg_logo} alt="Logo" style={{maxHeight: '50px', flexGrow: 1}} />
        </Box>
        
        {/* Spacer */}
        <Box flexGrow={1} />

        {/* Admin log in button - top right */}
        <Box marginRight={4}>
        <Button variant="text" color="inherit">Learn More</Button>
        </Box>
        <Button variant="contained" color="ochre">Admin Log In</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;