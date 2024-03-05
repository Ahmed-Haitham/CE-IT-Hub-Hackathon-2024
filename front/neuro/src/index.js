import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Header from './Header';
import AssessmentDivider from './AssessmentDivider';
import Assessment from './ActorAssessment';
import SymptomSelection from './SymptomSelect';
import FinalQuestions from './FinalQuestions';
import SendAssessment from './EndAssessment';
import Steps from './Footer';

import { createTheme } from '@mui/material/styles';
import { ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    ochre: {
      main: '#E3D026',
      light: '#E9DB5D',
      dark: '#A29415',
      contrastText: '#242105',
    },
  },
});

function App() {
  const [assessment_actor, setAssessmentActor] = React.useState({
    selectedActor: 'patient',
    // Add other state variables here for other components
  });

  const handleActorChange = (value) => {
    setAssessmentActor({ ...assessment_actor, selectedActor: value });
  };

  const handleSubmit = () => {
    const requestData = {
      selectedActor: assessment_actor.selectedActor,
      // Add other data properties as needed
    };

    fetch('http://localhost:8000/evaluateAssessment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add any other headers if needed
      },
      body: JSON.stringify(requestData),
    })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });
  };
  
  return (
    <React.StrictMode>
      <ThemeProvider theme={theme}>
        <Header />
        <AssessmentDivider text="Do the assessment as" />
        <Assessment selected={assessment_actor.selectedActor} handleToggle={handleActorChange}/>
        <AssessmentDivider text="Which symptoms are present?" />
        <SymptomSelection />
        <AssessmentDivider text="Now provide final details" />
        <FinalQuestions />
        <AssessmentDivider text="Are you ready to submit?" />
        <SendAssessment onSubmit={handleSubmit}/>
        <Steps />
      </ThemeProvider>
    </React.StrictMode>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
