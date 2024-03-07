import React from 'react';
import { Link } from 'react-router-dom'; 
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import Box from '@mui/material/Box';


const SendAssessment = ({ onSubmit }) => {

    const handleClick = () => {
        onSubmit(); // Call onSubmit function passed from parent component
    };

    return (
        <Box sx={{ padding: '0 2em', mb: 15, display: 'flex', justifyContent: 'center' }}>
            <Link to="/summary" style={{ textDecoration: 'none' }}> {/* Use Link component */}
                <Button
                    onClick={handleClick}
                    endIcon={<SendIcon />}
                    variant="contained"
                    >
                    <span>Finish Assessment</span>
                </Button>
            </Link>
        </Box>
    )
}
export default SendAssessment;