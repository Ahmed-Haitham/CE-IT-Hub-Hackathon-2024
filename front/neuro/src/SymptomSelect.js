import * as React from 'react';
import { Grid, Box, List, IconButton, ListItem, ListItemText, ToggleButton, ToggleButtonGroup } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import DeleteIcon from '@mui/icons-material/Delete';
import Switch from '@mui/material/Switch';
import useMediaQuery from '@mui/material/useMediaQuery';

export default function SymptomSelection() {
  const isSmallScreen = useMediaQuery(theme => theme.breakpoints.down('sm'));
  const [selected_progression, setSelectedProgression] = React.useState('stable');
  const [selected_symmetricity, setSelectedSymmetricity] = React.useState('na');
  const [selected_family_history, setSelectedFamilyHistory] = React.useState(false);
  const [selectedOptions, setSelectedOptions] = React.useState([]);

  const handleProgressionToggle = (value) => () => {
    setSelectedProgression(value);
  };

  const handleSymmetricityToggle = (value) => () => {
    setSelectedSymmetricity(value);
  };

  const familyHistoryToggle = (event) => {
    setSelectedFamilyHistory(event.target.checked);
  };

  const handleDelete = (optionToDelete) => () => {
    setSelectedOptions((options) => options.filter((option) => option.title !== optionToDelete.title));
  };

  async function getList() {
    const response = await fetch('http://localhost:8000/symptoms?distinct_only=true');
    // this works but the above does not: NetworkError when attempting to fetch resource.
    // const response = await fetch('https://jsonplaceholder.typicode.com/posts');
    const data = await response.json();
    return data;
  }  
  const [list_items, setListItems] = React.useState([]);
  React.useEffect(() => {
    getList().then(data => setListItems(data));
  }, []);

  return (
    <Box sx={{ padding: '0 2em', display: 'flex', justifyContent: 'center', flexDirection: 'column' }}>
      {/*Seacrhable, scrollable dropdown with autocomplete and delete chips
      can be enhanced to send requests after typing to search by tags as well
      https://mui.com/material-ui/react-autocomplete/#google-maps-place*/}
      <Autocomplete
        multiple
        limitTags={2}
        id="symptom-dropdown"
        options={list_items}
        getOptionLabel={(option) => option.title}
        defaultValue={[]}
        value={selectedOptions}
        onChange={(event, newValue) => {
          setSelectedOptions(newValue);
        }}
        filterOptions={(options, params) => {
          const filtered = options.filter((option) => {
            /*Untested, search by tags in response
            const tagsMatch = option.tags.some((tag) =>
              tag.toLowerCase().includes(params.inputValue.toLowerCase())
            );
            */
            const bodyMatch = option.body
              .toLowerCase()
              .includes(params.inputValue.toLowerCase());
            const titleMatch = option.title
              .toLowerCase()
              .includes(params.inputValue.toLowerCase());
            return bodyMatch || titleMatch;
            //turn tags search instead of body
            //return tagsMatch || titleMatch;
          });
          return filtered;
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
            <Grid item xs={3}><strong>Symptom</strong></Grid>
            <Grid item xs={3}><strong>Symptom Progression</strong></Grid>
            <Grid item xs={3}><strong>Symptom Symmetricity</strong></Grid>
            <Grid item xs={3}><strong>In Family History</strong></Grid>
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
                <ListItemText primary={option.title} />
              </Grid>
              {/*2nd item: box with progression choices group*/}
              <Grid item xs={3} flexDirection="row" alignItems="center">
                <ToggleButtonGroup 
                  value={selected_progression}
                  exclusive
                  onChange={handleProgressionToggle}
                  orientation={isSmallScreen ? 'vertical' : 'horizontal'}
                  aria-label="progression choice"
                  sx={{ marginRight: '1em', flexWrap: 'wrap' }}>
                  <ToggleButton
                    value="stable"
                    onChange={handleProgressionToggle('stable')}
                    aria-label="stable"
                  >
                    Stable
                  </ToggleButton>
                  <ToggleButton
                    value="variable"
                    onChange={handleProgressionToggle('variable')}
                    aria-label="variable"
                  >
                    Variable
                  </ToggleButton>
                </ToggleButtonGroup>
              </Grid>
              {/*3rd item: box with symmetricity choices group*/}
              <Grid item xs={3} flexDirection="row" alignItems="center">
                <ToggleButtonGroup 
                  value={selected_symmetricity}
                  onChange={handleSymmetricityToggle}
                  orientation={isSmallScreen ? 'vertical' : 'horizontal'}
                  aria-label="symmetricity"
                  sx={{ marginRight: '1em' , flexWrap: 'wrap' }}>
                  <ToggleButton
                    value="na"
                    onChange={handleSymmetricityToggle('na')}
                    aria-label="na"
                  >
                    NA
                  </ToggleButton>
                  <ToggleButton
                    value="unilateral"
                    onChange={handleSymmetricityToggle('unilateral')}
                    aria-label="unilateral"
                  >
                    1 Side
                  </ToggleButton>
                  <ToggleButton
                    value="bilateral"
                    onChange={handleSymmetricityToggle('bilateral')}
                    aria-label="bilateral"
                  >
                    2 Sides
                  </ToggleButton>
                </ToggleButtonGroup>
              </Grid>
              {/*4th item: switch for faimily history*/}
              <Grid item xs={3} flexDirection="row" alignItems="center">
                <Switch
                  checked={selected_family_history}
                  onChange={familyHistoryToggle}
                  name="selected_family_history"
                />
              </Grid>
            </Grid>
          </ListItem>
          ))}
        </List>
      </Box>
    </Box>
  );
}