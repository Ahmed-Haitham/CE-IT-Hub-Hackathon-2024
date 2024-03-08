import React from 'react';
import { useLocation } from 'react-router-dom';
import { Grid, Box, Button, Chip, Accordion, Typography } from '@mui/material';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';


const Predictions = () => {
    const location = useLocation();
    const data = location.state;
    const sortedPredictions = [...data.predicted].sort((a, b) => b.probability - a.probability);

    const getChipColor = (probability) => {
      if (probability < 50) return 'success';
      if (probability < 80) return 'warning';
      return 'error';
    };

    return (
      <Box sx={{ padding: '0 2em', mb: 4, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: 'center', mb: 2 }}>
            Predicted Diseases
          </Typography>
          {sortedPredictions.map((item, index) => (
            <Accordion key={index}>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1a-content"
                id="panel1a-header"
              >
                <Typography sx={{ flexGrow: 1 }}>{item.disease}</Typography>
                <Chip 
                  label={`${item.probability}%`} 
                  color={getChipColor(item.probability)}  
                  sx={{ mr: 3 }}
                />
              </AccordionSummary>
              <AccordionDetails>
                <Grid container direction="column">
                  <Grid item xs>
                    <Typography>
                      {/* TODO: Add a disease description here */}
                      Disease Description: {item.disease}
                    </Typography>
                  </Grid>
                  <Grid item xs align="right">
                    <Button 
                      id="learnMoreButton"
                      variant="contained" 
                      color="primary"
                      onClick={() => {
                        const url = item.disease_info_link 
                          ? item.disease_info_link 
                          : 'https://rarediseases.org/?s=' + item.disease;
                        window.open(url, '_blank');
                      }} 
                    >
                      Learn More
                    </Button>
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      );
  };

export default Predictions;