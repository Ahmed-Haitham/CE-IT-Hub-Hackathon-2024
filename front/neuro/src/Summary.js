import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import Theme from "./components/utils/Theme"

import Header from './components/utils/Header';
import AssessmentDivider from './components/utils/AssessmentDivider';
import Steps from './components/utils/Footer';

import Box from '@mui/material/Box';
import PrintAssessment from './components/summary_page/PrintAssessment';

import { useLocation } from 'react-router-dom';


const Summary = () => {
    const location = useLocation();
    const data = location.state;
      return (
        <Box sx={{ padding: '0 2em', display: 'flex', justifyCotent: 'center' }}>
          <div>
            {data.received.map((item, index) => (
              <div key={index}>
                <p>Symptom Medical Name: {item.symptom_medical_name}</p>
                <p>Symptom Progression: {item.symptom_progression}</p>
                {/* Render other properties as needed */}
              </div>
            ))}
            {data.predicted.map((item, index) => (
              <div key={index}>
                <p>Disease: {item.disease}</p>
                <p>Probability: {item.probability}</p>
                {/* Render other properties as needed */}
              </div>
            ))}
          </div>
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