import React from 'react';
import Divider from '@mui/material/Divider';

const AssessmentDivider = ({ text }) => {
    return(
        <Divider sx={{ mt: 4, mb: 4 }}>{text}</Divider>
    )
}

export default AssessmentDivider;