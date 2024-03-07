import Paper from '@mui/material/Paper';
import { ThemeProvider } from '@mui/material/styles';
import React from 'react';
import ReactDOM from 'react-dom/client';
import Assessment from './ActorAssessment';
import AssessmentDivider from './AssessmentDivider';
import { UserProvider } from "./context/UserContext";
import SendAssessment from './EndAssessment';
import FinalQuestions from './FinalQuestions';
import Steps from './Footer';
import Header from './Header';
import './index.css';
import SaveAssessment from './Save';
import SymptomSelection from './SymptomSelect';
import Theme from "./Theme";

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Login from './components/Login';
import Upload from './components/Upload';

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
};

// Add more links here
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "summary",
    element: <SummaryPage />,
  },
  {
    path: "login",
    element: <UserProvider><Login /></UserProvider>,
  },
  {
    path: "upload",
    element: <UserProvider><Upload /></UserProvider>,
  }
]);

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
  const handleSubmit = () => {
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

    fetch(`${process.env.REACT_APP_API_URL}/evaluateAssessment`, {
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
        <SendAssessment onSubmit={handleSubmit} />
        <Steps />
      </ThemeProvider>
    </React.StrictMode>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <RouterProvider router={router} />
);