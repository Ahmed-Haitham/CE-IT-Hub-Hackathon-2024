import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { ThemeProvider, styled } from '@mui/material/styles';
import React, { useState, useEffect } from "react";
import Header from "../utils/Header";
import Theme from "../utils/Theme";

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
  const [file, setFile] = useState(null);

  useEffect(() => {
    const uploadFile = async (file) => {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/uploadfile`, {
          method: 'POST',
          headers: {
            'accept': 'application/json',
            'Content-Type': 'multipart/form-data',
          },
          body: formData,
        });

        if (response.ok) {
          console.log("File uploaded successfully!");
        } else {
          console.error("Failed to upload file.");
        }
      } catch (error) {
        console.error(error);
      }
    };

    if (file) {
      uploadFile(file);
    }
  }, [file]);

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };


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
            <VisuallyHiddenInput type="file" onChange={handleFileUpload} />
          </Button>
          <Button
            variant="contained"
            startIcon={<CloudDownloadIcon />}
          >
            <a
              href="/data_template.xlsx"
              download="data_template.xlsx"
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              Download Template file to fill
            </a>
          </Button>
          { file && <p>{file.name}</p>}
        </Box>
      </ThemeProvider>
    </React.StrictMode>
  );
}