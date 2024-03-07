import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import Theme from "./components/utils/Theme"

import Header from './components/utils/Header';
import AssessmentDivider from './components/utils/AssessmentDivider';
import Steps from './components/utils/Footer';

import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import SaveAssessment from './components/user_inputs/EndAssessment';

const constructSummary = () => {
    // Customize the template based on your requirements
    // return `Since you have ${symptoms.join(', ')}, you probably have ${condition}.`;
    return `Since you have *some symptoms*, you should go to *doctor*.`;
  };


const SummaryContent = ({ summary }) => {
    return (
      <Paper variant="elevation">{'Since you have *some symptoms*, you should to to *doctor*.'}</Paper>
      // <Box sx={{ padding: '1em' }}>
      //   <Typography variant="body1">{summary}</Typography>
      // </Box>
    );
  };

const SummaryPage = () => {
    return (
      <React.StrictMode>
        <ThemeProvider theme={Theme}>
          <Header />
          <AssessmentDivider text="Summary" />
          <SummaryContent summary={constructSummary()} />
          <SaveAssessment />
        </ThemeProvider>
      </React.StrictMode>
    );
  }

export default SummaryPage;