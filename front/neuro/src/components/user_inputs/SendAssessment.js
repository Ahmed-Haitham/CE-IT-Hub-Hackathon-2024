import React from 'react';
import { Link } from 'react-router-dom'; 
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import Box from '@mui/material/Box';
import { useEffect } from 'react';

import { useNavigate } from 'react-router-dom';


const SendAssessment = ({ onSubmit }) => {

    const navigate = useNavigate();

    const handleClick = async () => {
        const result = await onSubmit();
        navigate("/summary", { state: result });
    };

    return (
        <Box sx={{ padding: '0 2em', mb: 15, display: 'flex', justifyContent: 'center' }}>
                <Button
                    onClick={()=>{handleClick()}}
                    endIcon={<SendIcon />}
                    variant="contained"
                    >
                    <span>Finish Assessment</span>
                </Button>
        </Box>
    )
}
export default SendAssessment;