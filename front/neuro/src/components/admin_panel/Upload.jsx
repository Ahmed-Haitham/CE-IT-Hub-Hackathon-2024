// TODO: API call
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Button from '@mui/material/Button';
import { ThemeProvider, styled } from '@mui/material/styles';
import * as React from 'react';
import Header from "../Header";
import Theme from "../utils/Theme";
import Box from '@mui/material/Box';
import Logout from './Logout';


const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

export default function Upload() {
  return (
    <React.StrictMode>
    <ThemeProvider theme={Theme}>
      <Header />
      <Box sx={{ padding: '0 2em', mb: 15, display: 'flex', justifyContent: 'center', mt: 10 }}>
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<CloudUploadIcon />}
      >
        Upload diseases data
        <VisuallyHiddenInput type="file" />
      </Button>
      </Box>
      <Logout />
    </ThemeProvider>
  </React.StrictMode>
    
  );
}