import React from 'react';
import { useEffect } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import Theme from "./components/utils/Theme"

import Header from './components/utils/Header';
import AssessmentDivider from './components/utils/AssessmentDivider';
import Steps from './components/utils/Footer';

import Assessment from './components/user_inputs/ActorAssessment';
import SymptomSelection from './components/user_inputs/SymptomSelect';
import FinalQuestions from './components/user_inputs/FinalQuestions';
import SendAssessment from './components/user_inputs/SendAssessment';

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
    //state for final questions
    const [female_gender, setSelectedGender] = React.useState([]);
    const [selected_ck, setSelectedCK] = React.useState({
      selectedCk: 'not_tested',
    });
    const [selected_age_onset, setSelectedAgeOnset] = React.useState({
      selectedAgeOnset: 'birth',
    });
  
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
    //functions for final questions
    const handleCKToggle = (value) => {
      setSelectedCK({ ...selected_ck, selectedCk: value });
    };
    const handleAgeOnsetToggle = (value) => {
      setSelectedAgeOnset({ ...selected_age_onset, selectedAgeOnset: value });
    };
    const handleGenderToggle = (index) => {
      setSelectedGender(prevState => {
        const newState = [...prevState];
        newState[index] = !newState[index];
        return newState;
      });
    };
  
    //function for submitting the assessment
    const handleSubmit = async () => {
      const requestData = {
        selectedActor: assessment_actor.selectedActor,
        selectedSymptoms: selected_dropdown_symptoms ? selected_dropdown_symptoms.map(symptom => symptom.symptom_medical_name) : [],
        selectedProgression: selected_progression,
        selectedSymmetricity: selected_symmetricity,
        selectedFamilyHistory: selected_family_history,
        selectedCk: selected_ck.selectedCk,
        selectedAgeOnset: selected_age_onset.selectedAgeOnset,
        female_gender: female_gender
      };
    
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/evaluateAssessment`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
        });
    
        const responseData = await response.json();
        return responseData;
      } catch (error) {
        console.error('Error:', error);
      }
    };
  
    return (
      <React.StrictMode>
        <ThemeProvider theme={Theme}>
          <Header />
          <AssessmentDivider text="Do the assessment as" />
          <Assessment
            selected={assessment_actor.selectedActor}
            handleToggle={handleActorChange}
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
          <FinalQuestions
            selected_ck={selected_ck.selectedCk}
            selected_age_onset={selected_age_onset.selectedAgeOnset}
            female_gender={female_gender}
            handleCKToggle={handleCKToggle}
            handleAgeOnsetToggle={handleAgeOnsetToggle}
            handleGenderToggle={handleGenderToggle}
            setSelectedGender={setSelectedGender}
          />
          <AssessmentDivider text="Are you ready to submit?" />
          <SendAssessment 
            onSubmit={handleSubmit} 
          />
          <Steps />
        </ThemeProvider>
      </React.StrictMode>
    );
  }

export default App;