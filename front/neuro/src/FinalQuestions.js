import * as React from 'react';
import useMediaQuery from '@mui/material/useMediaQuery';
import { Grid, ToggleButton, ToggleButtonGroup, Box } from '@mui/material';

const FinalQuestions = () => {
    const [selected_ck, setSelectedCK] = React.useState('not_tested');
    const [selected_age_onset, setSelectedAgeOnset] = React.useState('birth');
    const isSmallScreen = useMediaQuery(theme => theme.breakpoints.down('sm'));

    const handleCKToggle = (value) => () => {
        setSelectedCK(value);
    };

    const handleAgeOnsetToggle = (value) => () => {
        setSelectedAgeOnset(value);
    };

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
                                onChange={handleCKToggle('not_tested')}
                                aria-label="not_tested"
                            >
                            Untested
                            </ToggleButton>
                            <ToggleButton
                                value="normal"
                                selected={selected_ck === 'normal'}
                                onChange={handleCKToggle('normal')}
                                aria-label="normal"
                            >
                            Normal
                            </ToggleButton>
                            <ToggleButton
                                value="over_one_k"
                                selected={selected_ck === 'over_one_k'}
                                onChange={handleCKToggle('over_one_k')}
                                aria-label="over_one_k"
                            >
                            Over 1'000
                            </ToggleButton>
                            <ToggleButton
                                value="one_k_to_ten_k"
                                selected={selected_ck === 'one_k_to_ten_k'}
                                onChange={handleCKToggle('one_k_to_ten_k')}
                                aria-label="one_k_to_ten_k"
                            >
                            1'000 to 10'000
                            </ToggleButton>
                            <ToggleButton
                                value="over_ten_k"
                                selected={selected_ck === 'over_ten_k'}
                                onChange={handleCKToggle('over_ten_k')}
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
                                onChange={handleAgeOnsetToggle('birth')}
                                aria-label="birth"
                            >
                            Since birth
                            </ToggleButton>
                            <ToggleButton
                                value="under_ten"
                                selected={selected_age_onset === 'under_ten'}
                                onChange={handleAgeOnsetToggle('under_ten')}
                                aria-label="under_ten"
                            >
                            Under 10yo
                            </ToggleButton>
                            <ToggleButton
                                value="ten_to_twenty"
                                selected={selected_age_onset === 'ten_to_twenty'}
                                onChange={handleAgeOnsetToggle('ten_to_twenty')}
                                aria-label="ten_to_twenty"
                            >
                            10yo to 20yo
                            </ToggleButton>
                            <ToggleButton
                                value="twenty_to_thirty"
                                selected={selected_age_onset === 'twenty_to_thirty'}
                                onChange={handleAgeOnsetToggle('twenty_to_thirty')}
                                aria-label="twenty_to_thirty"
                            >
                            20yo to 30yo
                            </ToggleButton>
                            <ToggleButton
                                value="thirty_to_fifty"
                                selected={selected_age_onset === 'thirty_to_fifty'}
                                onChange={handleAgeOnsetToggle('thirty_to_fifty')}
                                aria-label="thirty_to_fifty"
                            >
                            30yo to 50yo
                            </ToggleButton>
                            <ToggleButton
                                value="over_fifty"
                                selected={selected_age_onset === 'over_fifty'}
                                onChange={handleAgeOnsetToggle('over_fifty')}
                                aria-label="over_fifty"
                            >
                            Over 50yo
                            </ToggleButton>
                        </ToggleButtonGroup>
                    </Grid>
                </Grid>
            </Box>
        </React.Fragment>
    )}

export default FinalQuestions;