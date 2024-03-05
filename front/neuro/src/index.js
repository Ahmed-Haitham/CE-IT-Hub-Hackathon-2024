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
import reportWebVitals from './reportWebVitals';
import { createTheme } from '@mui/material/styles';
import { ThemeProvider } from '@mui/material/styles';

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

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

const MainPage = () => {
  return (
    <React.StrictMode>
      <ThemeProvider theme={theme}>
        <Header />
        <AssessmentDivider text="Do the assessment as" />
        <Assessment />
        <AssessmentDivider text="Which symptoms are present?" />
        <SymptomSelection />
        <AssessmentDivider text="Now provide final details" />
        <FinalQuestions />
        <AssessmentDivider text="Are you ready to submit?" />
        <SendAssessment />
        <Steps />
      </ThemeProvider>
    </React.StrictMode>
  );
};

const SummaryPage = () => {
  return (
    <React.StrictMode>
      <ThemeProvider theme={theme}>
        <Header />
        <AssessmentDivider text="Summary" />
        <SendAssessment/>
      </ThemeProvider>
    </React.StrictMode>
  );
};

// Add more links here
const router = createBrowserRouter([
  {
    path: "/",
    element: <MainPage />,
  },
  {
    path: "summary",
    element: <SummaryPage />,
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <RouterProvider router={router}/>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
