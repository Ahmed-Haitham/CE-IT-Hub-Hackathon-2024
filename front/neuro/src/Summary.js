import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import Theme from "./components/utils/Theme"
import { useLocation } from 'react-router-dom';

import Header from './components/utils/Header';
import AssessmentDivider from './components/utils/AssessmentDivider';
import Steps from './components/utils/Footer';

import { Grid, Box, Button, Chip, Accordion, Typography } from '@mui/material';
import PrintAssessment from './components/summary_page/PrintAssessment';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const Summary = () => {
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
                  label={`${item.probability * 100}%`} 
                  color={getChipColor(item.probability * 100)}  
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
                      onClick={() => window.open('https://rarediseases.org/?s=' + item.disease, '_blank')} 
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

const SummaryPage = () => {
    return (
      <React.StrictMode>
        <ThemeProvider theme={Theme}>
          <Header />
          <AssessmentDivider text="Summary" />
          <Summary />
          <PrintAssessment />
          <Steps
            step_number={1}
          />
        </ThemeProvider>
      </React.StrictMode>
    );
  }

export default SummaryPage;