import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import SummaryPage from './Summary';
import Login from './Login';
import Upload from './components/admin_panel/Upload'
import { UserProvider } from './components/utils/UserContext'

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

// Add more links here
const router = createBrowserRouter([
  {
    path: "/",
    element: <UserProvider><App /></UserProvider>,
  },
  {
    path: "summary",
    element: <UserProvider><SummaryPage /></UserProvider>,
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

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <RouterProvider router={router} />
);