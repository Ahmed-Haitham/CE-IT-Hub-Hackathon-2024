import * as React from 'react';
import LoadingButton from '@mui/lab/LoadingButton';
import SendIcon from '@mui/icons-material/Send';
import Box from '@mui/material/Box';

const SendAssessment = ({ onSubmit }) => {
    
    const [loading, setLoading] = React.useState(false);

    const handleClick = () => {
        setLoading(true);
        onSubmit(); // Call onSubmit function passed from parent component
    };

    return (
        <Box sx={{ padding: '0 2em', mb: 15, display: 'flex', justifyContent: 'center' }}>
        <LoadingButton
            onClick={handleClick}
            endIcon={<SendIcon />}
            loading={loading}
            loadingPosition="end"
            variant="contained"
        >
            <span>Finish Assessment</span>
        </LoadingButton>
        </Box>
    )
}
export default SendAssessment;