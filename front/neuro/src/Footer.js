import * as React from 'react';
import { Grid, Box, Stepper, Step, StepLabel, Typography, Container} from '@mui/material';

const Steps = () => {
    const steps = [
        'Fill in symptom details',
        'Receive your assessment',
      ];
    return (
      <Box
        sx={{
          bgcolor: 'background.paper',
          color: 'text.secondary',
          py: 2,
          borderTop: '1px solid',
          borderColor: 'divider',
        }}
      >
        <Container maxWidth={false}>
          <Grid container spacing={2} justifyContent="space-between">
          <Box sx={{ width: '100%' }}>
          <p></p>
            <Stepper activeStep={0} alternativeLabel>
                {steps.map((label) => (
                <Step key={label}>
                    <StepLabel>{label}</StepLabel>
                </Step>
                ))}
            </Stepper>
            <p></p>
            </Box>
            <Grid >
              <Typography variant="subtitle1" color="text.primary" gutterBottom>
                Disclaimer: This tool is not intended to replace a doctor's diagnosis of neural disease. Rather, it can be helpful to point you to the right specialist to consult.
              </Typography>
            </Grid>
        </Grid>   
        </Container>
      </Box>
    );
  };
  
  export default Steps;