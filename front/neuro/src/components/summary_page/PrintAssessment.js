// import * as React from 'react';
import React from 'react';
import { Link } from 'react-router-dom'; 
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';

const PrintAssessment = () => {
    const [showAlert, setShowAlert] = React.useState(false);
    const [open, setOpen] = React.useState(true);
    function handleClick() {
        setShowAlert(true);
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '10vh' }}>
            <Box sx={{ flex: '1 0 auto', padding: '0 2em', display: 'flex', justifyContent: 'center' }}>
                <Link to="/summary" style={{ textDecoration: 'none' }}>
                    <Button
                        onClick={handleClick}
                        endIcon={<SendIcon />}
                        variant="contained"
                    >
                        <span>Save/Print</span>
                    </Button>
                </Link>
            </Box>
            <Box sx={{ padding: '0 2em', marginTop: 'auto' }}>
                {showAlert && (
                    <Alert severity="success" onClose={() => setShowAlert(false)}>
                        Successfully Saved/Printed your response.
                    </Alert>
                )}
            </Box>
        </Box>
    )
}
export default PrintAssessment;