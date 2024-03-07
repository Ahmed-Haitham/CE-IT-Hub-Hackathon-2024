import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import Theme from "./components/utils/Theme"

import Header from './components/utils/Header';
import AssessmentDivider from './components/utils/AssessmentDivider';
import Steps from './components/utils/Footer';

import PredictedDiseases from './components/summary_page/PredictedDiseases';
import PrintAssessment from './components/summary_page/PrintAssessment';
import Selections from './components/summary_page/UserSelections';

const SummaryPage = () => {
    return (
      <React.StrictMode>
        <ThemeProvider theme={Theme}>
          <Header />
          <AssessmentDivider text="Summary" />
          <PredictedDiseases />
          <Selections />
          <PrintAssessment />
          <Steps
            step_number={1}
          />
        </ThemeProvider>
      </React.StrictMode>
    );
  }

export default SummaryPage;