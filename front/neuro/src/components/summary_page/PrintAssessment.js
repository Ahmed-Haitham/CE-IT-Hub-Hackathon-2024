// import * as React from 'react';
import React, { Fragment } from 'react';
import { Link } from 'react-router-dom'; 
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';

const PrintAssessment = () => {
    const [showAlert, setShowAlert] = React.useState(false);
    function handleClick() {
        setShowAlert(true);
        window.print();
    }

    return (
        <Fragment>
        <Box>
        <Box sx={{ padding: '0 2em', display: 'flex', justifyContent: 'center' }}>
                    <Button
                        onClick={handleClick}
                        endIcon={<SendIcon />}
                        variant="contained"
                    >
                        <span>Save/Print</span>
                    </Button>
            </Box>
        </Box>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '10vh' }}>
            <Box sx={{ padding: '0 2em', marginTop: 'auto' }}>
                {showAlert && (
                    <Alert severity="success" onClose={() => setShowAlert(false)}>
                        Successfully Saved/Printed your response.
                    </Alert>
                )}
            </Box>
        </Box>
        </Fragment>
    )
}
export default PrintAssessment;