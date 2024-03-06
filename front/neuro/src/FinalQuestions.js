import * as React from 'react';
import useMediaQuery from '@mui/material/useMediaQuery';
import { Grid, ToggleButton, ToggleButtonGroup, Box } from '@mui/material';

import { styled } from '@mui/material/styles';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

const FinalQuestions = ({selected_ck, selected_age_onset, handleCKToggle, handleAgeOnsetToggle, female_gender, handleGenderToggle, setSelectedGender}) => {
    const isSmallScreen = useMediaQuery(theme => theme.breakpoints.down('sm'));
    
    React.useEffect(() => {
        setSelectedGender(new Array(1).fill(true));
      }, []);

    //https://www.iloveimg.com/crop-image - Crop the image
    //https://convertio.co/jpg-svg/ - Convert to svg
    //https://www.svgviewer.dev/ - Use optimize here and pay attention to the viewBox settings
    const MaterialUISwitch = styled(Switch)(({ theme }) => ({
        width: 62,
        height: 34,
        padding: 7,
        '& .MuiSwitch-switchBase': {
          margin: 1,
          padding: 0,
          transform: 'translateX(6px)',
          '&.Mui-checked': {
            color: '#fff',
            transform: 'translateX(22px)',
            '& .MuiSwitch-thumb:before': {
              backgroundImage: `url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 803 1325"><path fill="${encodeURIComponent(
                '#fff',
              )}" d="m219.5 68-28 28-19-19-19-19-31 31-31 31 19 19 19 19-28.3 28.3L73 214.5l31 31 31 31 28.3-28.3 28.2-28.2 24.8 24.8c13.6 13.6 24.7 25 24.7 25.5 0 .4-2.7 6.2-5.9 12.9-18.7 39-22.9 80.9-12.2 122.5 23.2 90.1 114.5 146.9 206.4 128.3 22.6-4.6 48-15.6 66.7-28.8 12.2-8.5 33.6-29.9 42.3-42.2 8.3-11.7 19.5-34.1 23.7-47.5 16.6-52.6 9-107.5-20.9-152.6-26.5-39.8-66.7-66.4-115.1-76-9.6-2-14.7-2.3-31.5-2.4-21.1 0-27.7.8-45 5.2-12.7 3.3-25.3 8.1-36.7 14l-9 4.6-25.1-25.1-25.2-25.2 28-28 28-28-31-31-31-31zM415 274.1c16.5 3.8 35.3 15.2 46.2 28 15.6 18.4 22.6 38.6 21.5 62.3-.6 14.1-2.5 21.9-7.8 33.4-14.1 30.5-42.9 50.1-76.1 51.9-44.5 2.4-83.4-27.6-92.5-71.5-1.9-9.5-1.3-31.6 1.2-40.7 2.7-9.8 10.8-25.4 17.2-33 22.9-27.2 55.9-38.3 90.3-30.4m-37.5 306.6c-27.3 5.8-50.3 23.3-63.8 48.5-9.9 18.5-255.3 501.7-257.4 506.9-11.3 28-8.1 60.7 8.4 86.4 13.4 20.8 32.4 34.5 56.9 41.3l9.9 2.7 258.5.3c178.4.2 261.8 0 269.1-.8 13.6-1.3 23.2-4 34.4-9.5 21.6-10.7 39.6-31.1 47.6-54.3 6.9-19.8 6.6-44.6-.7-64-3.5-9.4-258-509.3-263.8-518.2-12.6-19.4-35.1-34.5-58.8-39.4-9.8-2-30.7-2-40.3.1"/></svg>')`,
            },
            '& + .MuiSwitch-track': {
              opacity: 1,
              backgroundColor: theme.palette.mode === 'dark' ? '#8796A5' : '#aab4be',
            },
          },
        },
        '& .MuiSwitch-thumb': {
          backgroundColor: theme.palette.mode === 'dark' ? '#003892' : '#001e3c',
          width: 32,
          height: 32,
          '&::before': {
            content: "''",
            position: 'absolute',
            width: '100%',
            height: '100%',
            left: 0,
            top: 0,
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center',
            backgroundImage: `url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 750 1253"><path fill="${encodeURIComponent(
              '#fff',
            )}" d="M442.6 27.3c-.6 4.8-4.6 83-4.3 83.3.1.1 16 1 35.2 1.9 19.3.9 35.8 2 36.8 2.3 1.4.6-3.2 5.6-22.6 25l-24.3 24.3-9.1-4.5c-37.7-18.5-82.1-22.5-123.8-11.1-61 16.6-109.3 66.4-124.4 128.3-4 16.5-5.5 31.6-4.8 49.1 4.3 108.9 105.1 187.7 212.2 166 64.7-13.2 118.5-63.9 135-127.5 5.9-22.6 7.4-49.7 4-71.8-3.1-20.5-11.2-44.1-21.2-61.4l-4.1-7 23.9-23.8c13.2-13.1 23.9-23.2 23.9-22.4 0 1.1 3.9 73.4 4 73.5.2.3 86.5-4.7 86.8-5 .4-.4-9.2-190.2-10.4-205l-.5-7.1-103.2-5.2c-56.8-2.9-104.4-5.5-105.9-5.7-2.5-.4-2.7-.1-3.2 3.8m-43.7 204.8c41.5 9.5 70.3 48.7 67.8 92.3-1.3 22.7-10.7 42.7-27.3 58.7-11.5 10.9-21.8 16.9-37.1 21.6-7.8 2.3-10.6 2.6-23.8 2.7-12.7.1-16.3-.3-23.3-2.2-26.2-7.1-46.9-24.4-58.1-48.3-12.4-26.6-11.3-57.2 3.2-82.9 6-10.6 21.6-26.2 32.4-32.3 20.6-11.7 42.9-14.9 66.2-9.6M104.6 538.6c-29 6.3-53.2 25.7-66.3 53.3-10.7 22.6-11.7 50.9-2.6 73.8 1.3 3.5 12.2 25.5 24.2 49 12 23.6 30.9 60.8 42.1 82.8 11.1 22 25.3 49.9 31.5 62s19.2 37.7 29 57c9.8 19.2 22.4 44 28 55s17.8 34.8 27 53c23.6 46.4 42.7 84 61 120 21.6 42.4 25 47.5 40.4 59.7 23 18.4 55.4 24.8 84.6 16.8 20.7-5.6 40-19.3 52.1-37 2.8-4.1 12.6-22.4 21.9-40.5 9.2-18.2 23.5-46.3 31.8-62.5 8.2-16.2 20.2-39.9 26.7-52.5 6.5-12.7 19.3-37.9 28.5-56 26.6-52.3 46.9-92.3 58.5-115 5.9-11.6 20.1-39.5 31.5-62 11.4-22.6 23.8-46.9 27.5-54 21.8-42 38.1-75.8 40.6-84 2.5-8.1 2.8-10.5 2.8-25 .1-18-1-23.8-7.3-38.5-5.1-11.8-10.9-20-21.5-30.5-12-11.7-24.3-18.9-42.2-24.2-5.6-1.7-19.8-1.8-274.4-2-233.7-.1-269.4 0-275.4 1.3"/></svg>')`,
          },
        },
        '& .MuiSwitch-track': {
          opacity: 1,
          backgroundColor: theme.palette.mode === 'dark' ? '#8796A5' : '#aab4be',
          borderRadius: 20 / 2,
        },
      }));      

    return (
        <React.Fragment>
            <Box sx={{ padding: '0 2em', display: 'flex', justifyContent: 'center' }}>
                <Grid container spacing={3} alignItems="center" >
                    <Grid item xs={3}>
                        <p>Select your CK Level</p>
                    </Grid>
                    <Grid item xs={9}>
                        <ToggleButtonGroup
                            value={selected_ck}
                            exclusive
                            onChange={handleCKToggle}
                            orientation={isSmallScreen ? 'vertical' : 'horizontal'}
                            aria-label="ck level"
                            >
                            <ToggleButton
                                value="not_tested"
                                selected={selected_ck === 'not_tested'}
                                onChange={() => handleCKToggle('not_tested')}
                                aria-label="not_tested"
                            >
                            Untested
                            </ToggleButton>
                            <ToggleButton
                                value="normal"
                                selected={selected_ck === 'normal'}
                                onChange={() => handleCKToggle('normal')}
                                aria-label="normal"
                            >
                            Normal
                            </ToggleButton>
                            <ToggleButton
                                value="over_one_k"
                                selected={selected_ck === 'over_one_k'}
                                onChange={() => handleCKToggle('over_one_k')}
                                aria-label="over_one_k"
                            >
                            Over 1'000
                            </ToggleButton>
                            <ToggleButton
                                value="one_k_to_ten_k"
                                selected={selected_ck === 'one_k_to_ten_k'}
                                onChange={() => handleCKToggle('one_k_to_ten_k')}
                                aria-label="one_k_to_ten_k"
                            >
                            1'000 to 10'000
                            </ToggleButton>
                            <ToggleButton
                                value="over_ten_k"
                                selected={selected_ck === 'over_ten_k'}
                                onChange={() => handleCKToggle('over_ten_k')}
                                aria-label="over_ten_k"
                            >
                            Over 10'000
                            </ToggleButton>
                        </ToggleButtonGroup>
                    </Grid>
                </Grid>
            </Box>
            <p></p>
            <Box sx={{ padding: '0 2em', display: 'flex', justifyContent: 'center' }}>
                <Grid container spacing={3} alignItems="center" >
                    <Grid item xs={3}>
                        <p>Select your age when you had the first symptom</p>
                    </Grid>
                    <Grid item xs={9}>
                        <ToggleButtonGroup
                            value={selected_age_onset}
                            exclusive
                            onChange={handleAgeOnsetToggle}
                            orientation={isSmallScreen ? 'vertical' : 'horizontal'}
                            aria-label="ck level"
                            >
                            <ToggleButton
                                value="birth"
                                selected={selected_age_onset === 'birth'}
                                onChange={() => handleAgeOnsetToggle('birth')}
                                aria-label="birth"
                            >
                            Since birth
                            </ToggleButton>
                            <ToggleButton
                                value="under_ten"
                                selected={selected_age_onset === 'under_ten'}
                                onChange={() => handleAgeOnsetToggle('under_ten')}
                                aria-label="under_ten"
                            >
                            Under 10yo
                            </ToggleButton>
                            <ToggleButton
                                value="ten_to_twenty"
                                selected={selected_age_onset === 'ten_to_twenty'}
                                onChange={() => handleAgeOnsetToggle('ten_to_twenty')}
                                aria-label="ten_to_twenty"
                            >
                            10yo to 20yo
                            </ToggleButton>
                            <ToggleButton
                                value="twenty_to_thirty"
                                selected={selected_age_onset === 'twenty_to_thirty'}
                                onChange={() => handleAgeOnsetToggle('twenty_to_thirty')}
                                aria-label="twenty_to_thirty"
                            >
                            20yo to 30yo
                            </ToggleButton>
                            <ToggleButton
                                value="thirty_to_fifty"
                                selected={selected_age_onset === 'thirty_to_fifty'}
                                onChange={() => handleAgeOnsetToggle('thirty_to_fifty')}
                                aria-label="thirty_to_fifty"
                            >
                            30yo to 50yo
                            </ToggleButton>
                            <ToggleButton
                                value="over_fifty"
                                selected={selected_age_onset === 'over_fifty'}
                                onChange={() => handleAgeOnsetToggle('over_fifty')}
                                aria-label="over_fifty"
                            >
                            Over 50yo
                            </ToggleButton>
                        </ToggleButtonGroup>
                    </Grid>
                </Grid>
            </Box>
            <p></p>
            <Box sx={{ padding: '0 2em', display: 'flex', justifyCotent: 'center' }}>
                <Grid container spacing={3} alignItems="center" >
                    <Grid item xs={3}>
                        <p>Select your gender</p>
                    </Grid>
                    <Grid item xs={9}>
                        <Stack direction="row" spacing={1} alignItems="center">
                            <Typography>Male</Typography>
                            <MaterialUISwitch 
                                checked={female_gender[0]}
                                onChange={() => handleGenderToggle(0)}
                                inputProps={{ 'aria-label': 'gender_toggle' }} />
                            <Typography>Female</Typography>
                        </Stack>
                    </Grid>
                </Grid>
            </Box>
        </React.Fragment>
    )}

export default FinalQuestions;