import Button from '@mui/material/Button';
import React from "react";
import { Link } from 'react-router-dom';

const LoginButton = () => {

  return (
    <Button variant="contained" color="ochre" as={Link} to="/login" style={{ textDecoration: 'none' }}>
      ADMIN LOG IN
    </Button>
  );
};

export default LoginButton;
