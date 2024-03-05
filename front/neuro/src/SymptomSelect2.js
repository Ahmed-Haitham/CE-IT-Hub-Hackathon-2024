import * as React from 'react';
import { Grid, Box, List, IconButton, ListItem, ListItemText, ToggleButton, ToggleButtonGroup } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import DeleteIcon from '@mui/icons-material/Delete';
import Switch from '@mui/material/Switch';
import useMediaQuery from '@mui/material/useMediaQuery';

export default function SymptomSelection2() {
    const isSmallScreen = useMediaQuery(theme => theme.breakpoints.down('sm'));
    const [selectedOptions, setSelectedOptions] = React.useState([]);
    const [familyHistoryStates, setFamilyHistoryStates] = React.useState([]);
    const [progressionStates, setProgressionStates] = React.useState([]);
  
    async function getList() {
      const response = await fetch('http://localhost:8000/symptoms?distinct_only=true');
      const data = await response.json();
      return data;
    }  
  
    const [list_items, setListItems] = React.useState([]);
    React.useEffect(() => {
      getList().then(data => setListItems(data));
    }, []);
  
    // Function to initialize the array of family history states
    React.useEffect(() => {
      setFamilyHistoryStates(new Array(selectedOptions.length).fill(false));
    }, [selectedOptions]);
  
    // Function to toggle the state of a family history switch
    const familyHistoryToggle = (index) => {
      setFamilyHistoryStates(prevState => {
        const newState = [...prevState];
        newState[index] = !newState[index];
        return newState;
      });
    };

    React.useEffect(() => {
        setProgressionStates(new Array(selectedOptions.length).fill('stable'));
      }, [selectedOptions]);

    const progressionToggle = (index, value) => () => {
        setProgressionStates(prevState => {
            const newState = [...prevState];
            newState[index] = value;
            return newState;
        });
    };
  
    //TODO: Delete needs to make sure length of symptoms=lenght of selections
    const handleDelete = (optionToDelete) => () => {
        setSelectedOptions((options) => options.filter((option) => option.symptom_medical_name !== optionToDelete.symptom_medical_name));
    }
  
    return (
      <Box sx={{ padding: '0 2em', display: 'flex', justifyContent: 'center', flexDirection: 'column' }}>
        {/*Seacrhable, scrollable dropdown with autocomplete and delete chips*/}
        <Autocomplete
          multiple
          limitTags={2}
          id="symptom-dropdown"
          options={list_items}
          getOptionLabel={(option) => option.symptom_medical_name}
          defaultValue={[]}
          value={selectedOptions}
          onChange={(event, newValue) => {
            setSelectedOptions(newValue);
          }}
          renderInput={(params) => (
            <TextField {...params} label="Symptoms" placeholder="Type a symptom" />
          )}
          sx={{ width: '95%' }}
        />
        {/*Padded box for list of selections and attribute editing*/}
        <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '1em' }}>
          <List>
            <Grid container spacing={3}>
              <Grid item xs={3}><strong>In Family History</strong></Grid>
              <Grid item xs={3}><strong>Symptom Progression</strong></Grid>
            </Grid>
            {/*List contains multiselect selections*/}
            {selectedOptions.map((option, index) => (
            <ListItem key={index}>
              {/*1st item: delete button*/}
              <Grid container spacing={3}>
                <Grid item xs={3} container direction="row" alignItems="center">
                  {/*1-A item: delete button*/}
                  <IconButton edge="start" aria-label="delete" onClick={handleDelete(option)}>
                    <DeleteIcon />
                  </IconButton>
                  {/*1-B item: symptom text*/}
                  <ListItemText primary={option.symptom_medical_name} />
                </Grid>
                {/*2nd item: switch for family history*/}
                <Grid item xs={3} flexDirection="row" alignItems="center">
                  <Switch
                    checked={familyHistoryStates[index]}
                    onChange={() => familyHistoryToggle(index)}
                    name={`selected_family_history_${index}`}
                  />
                </Grid>
                <Grid item xs={3} flexDirection="row" alignItems="center">
                <ToggleButtonGroup 
                  value={progressionStates[index]}
                  exclusive
                  onChange={progressionToggle}
                  orientation={isSmallScreen ? 'vertical' : 'horizontal'}
                  aria-label="progression choice"
                  sx={{ marginRight: '1em', flexWrap: 'wrap' }}>
                  <ToggleButton
                    value="stable"
                    onChange={progressionToggle(index, 'stable')}
                    aria-label="stable"
                  >
                    Stable
                  </ToggleButton>
                  <ToggleButton
                    value="variable"
                    onChange={progressionToggle(index, 'variable')}
                    aria-label="variable"
                  >
                    Variable
                  </ToggleButton>
                  <ToggleButton
                    value="progressing"
                    onChange={progressionToggle(index, 'progressing')}
                    aria-label="progressing"
                  >
                    Progressing
                  </ToggleButton>
                </ToggleButtonGroup>
              </Grid>
              </Grid>
            </ListItem>
            ))}
          </List>
        </Box>
      </Box>
    );
  }
  