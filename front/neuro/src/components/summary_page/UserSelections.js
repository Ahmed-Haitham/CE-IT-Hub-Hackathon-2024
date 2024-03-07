import React, { Fragment } from 'react';
import { useLocation } from 'react-router-dom';
import { Grid, Box, Button, Chip, Typography, Accordion, AccordionDetails, AccordionSummary } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import useMediaQuery from '@mui/material/useMediaQuery';

const Selections = () => {
    const location = useLocation();
    const data = location.state;
    console.log(data.received);
    let firstDict = data.received[0];
    let gender = firstDict['gender'];
    let ck = firstDict['test_ck_level'];
    let onset = firstDict['first_symptom_age_onset_group'];
    const matches = useMediaQuery(theme => theme.breakpoints.down('sm'));

    return (
        <Box sx={{ padding: '0 2em', mb: 4, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <Box>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: 'center', mb: 2 }}>
                    Based on User Selections
                </Typography>
                {data.received.map((item, index) => (
                    <Accordion key={index}>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            >
                            <Typography sx={{ flexGrow: 1 }}>{item.symptom_medical_name}</Typography>
                            <Box>
                                <Chip label={`Symmetricity: ${item.symptom_symmetricity}`} sx={{ mr: 1 }}/>
                                <Chip label={`Progression: ${item.symptom_progression}`} sx={{ mr: 1 }}/>
                                <Chip label={`In Family History: ${item.symptom_in_family_history ? 'Yes' : 'No'}`} sx={{ mr: 1 }}/>
                            </Box>
                        </AccordionSummary>
                        <AccordionDetails>
                            Description: {item.symptom_description}
                        </AccordionDetails>
                    </Accordion>
                ))}
                <p></p>
                <Box style={{ 
                    display: 'flex', 
                    gap: '10px', 
                    flexDirection: matches ? 'column' : 'row', 
                    alignItems: 'center', 
                    justifyContent: 'center' 
                }}>
                    <Chip 
                        label={<Typography variant="subtitle1">{`Gender: ${gender}`}</Typography>} 
                        size="medium"
                    />
                    <Chip 
                        label={<Typography variant="subtitle1">{`CK Level: ${ck}`}</Typography>} 
                        size="medium"
                    />
                    <Chip 
                        label={<Typography variant="subtitle1">{`First Symptom Age of Onset: ${onset}`}</Typography>} 
                        size="medium"
                    />
                </Box>
            </Box>
        </Box>
    );
};

export default Selections;