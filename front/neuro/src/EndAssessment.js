import React from 'react';
import { Link } from 'react-router-dom'; 
import LoadingButton from '@mui/lab/LoadingButton';
import SendIcon from '@mui/icons-material/Send';
import Box from '@mui/material/Box';

const SendAssessment = () => {
    const [loading, setLoading] = React.useState(false);

    function handleClick() {
        setLoading(true);
    }

    return (
        <Box sx={{ padding: '0 2em', mb: 15, display: 'flex', justifyContent: 'center' }}>
            <Link to="/summary" style={{ textDecoration: 'none' }}> {/* Use Link component */}
                <LoadingButton
                    onClick={handleClick}
                    endIcon={<SendIcon />}
                    loading={loading}
                    loadingPosition="end"
                    variant="contained"
                    >
                    <span>Finish Assessment</span>
                </LoadingButton>
            </Link>
        </Box>
    )
}
export default SendAssessment;