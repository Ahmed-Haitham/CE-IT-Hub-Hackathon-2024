import React from 'react';
import { ToggleButton, ToggleButtonGroup, Box } from '@mui/material';
import useMediaQuery from '@mui/material/useMediaQuery';
import HealingIcon from '@mui/icons-material/Healing';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import SchoolIcon from '@mui/icons-material/School';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';

const AssessmentActor = ({ selected, handleToggle }) => {
  const isSmallScreen = useMediaQuery(theme => theme.breakpoints.down('sm'));

  return (
    <Box sx={{ padding: '0 2em', display: 'flex', justifyContent: 'center' }}>
      <ToggleButtonGroup
        value={selected}
        exclusive
        onChange={handleToggle}
        orientation={isSmallScreen ? 'vertical' : 'horizontal'}
        aria-label="actor"
      >
        <ToggleButton
          value="patient"
          selected={selected === 'patient'}
          onChange={() => handleToggle('patient')}
          aria-label="patient"
        >
          <Box marginRight={2} display="flex" alignItems="center">
          <HealingIcon />
          </Box>
          Patient
        </ToggleButton>
        <ToggleButton
          value="family"
          selected={selected === 'family'}
          onChange={() => handleToggle('family')}
          aria-label="family"
        >
          <Box marginRight={2} display="flex" alignItems="center">
          <FamilyRestroomIcon />
          </Box>
          Family Member
        </ToggleButton>
        <ToggleButton
          value="student"
          selected={selected === 'student'}
          onChange={() => handleToggle('student')}
          aria-label="student"
        >
          <Box marginRight={2} display="flex" alignItems="center">
          <SchoolIcon />
          </Box>
          Student
        </ToggleButton>
        <ToggleButton
          value="doctor"
          selected={selected === 'doctor'}
          onChange={() => handleToggle('doctor')}
          aria-label="doctor"
        >
          <Box marginRight={2} display="flex" alignItems="center">
          <LocalHospitalIcon />
          </Box>
          Medical Professional
        </ToggleButton>
      </ToggleButtonGroup>
    </Box>
  );
};

export default AssessmentActor;