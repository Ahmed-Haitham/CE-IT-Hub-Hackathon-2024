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
  //state for actor selection
  const [assessment_actor, setAssessmentActor] = React.useState({
    selectedActor: 'patient',
  });
  //state for symptom selection
  const [selected_progression, setSelectedProgression] = React.useState([]);
  const [selected_symmetricity, setSelectedSymmetricity] = React.useState([]);
  const [selected_family_history, setSelectedFamilyHistory] = React.useState([]);
  const [selected_dropdown_symptoms, setSelectedDropdownSelection] = React.useState([]);

  //function for actor selection
  const handleActorChange = (value) => {
    setAssessmentActor({ ...assessment_actor, selectedActor: value });
  };
  //functions for symptom selection
  const handleProgressionToggle = (index, value) => () => {
    setSelectedProgression(prevState => {
        const newState = [...prevState];
        newState[index] = value;
        return newState;
    });
  };
  const handleSymmetricityToggle = (index, value) => () => {
    setSelectedSymmetricity(prevState => {
        const newState = [...prevState];
        newState[index] = value;
        return newState;
    });
  };
  const familyHistoryToggle = (index) => {
    setSelectedFamilyHistory(prevState => {
      const newState = [...prevState];
      newState[index] = !newState[index];
      return newState;
    });
  };
  
  //function for submitting the assessment
  const handleSubmit = () => {
    const requestData = {
      selectedActor: assessment_actor.selectedActor,
      selectedSymptoms: selected_dropdown_symptoms ? selected_dropdown_symptoms.map(symptom => symptom.symptom_medical_name) : [],
      selectedProgression: selected_progression,
      selectedSymmetricity: selected_symmetricity,
      selectedFamilyHistory: selected_family_history,
      //TODO: Add the rest of the data
    };

    fetch('http://localhost:8000/evaluateAssessment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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
        <Assessment 
          selected={assessment_actor.selectedActor} handleToggle={handleActorChange}
        />
        <AssessmentDivider text="Which symptoms are present?" />
        <SymptomSelection 
          handleProgressionToggle={handleProgressionToggle}
          handleSymmetricityToggle={handleSymmetricityToggle}
          familyHistoryToggle={familyHistoryToggle}
          selected_progression={selected_progression}
          selected_symmetricity={selected_symmetricity}
          selected_family_history={selected_family_history}
          selectedOptions={selected_dropdown_symptoms}
          setSelectedProgression={setSelectedProgression}
          setSelectedSymmetricity={setSelectedSymmetricity}
          setSelectedFamilyHistory={setSelectedFamilyHistory}
          setSelectedOptions={setSelectedDropdownSelection}
        />
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
