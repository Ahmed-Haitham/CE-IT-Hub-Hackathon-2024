import * as React from 'react';
import { Grid, Box, List, IconButton, ListItem, ListItemText, ToggleButton, ToggleButtonGroup, MenuItem, Select } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import DeleteIcon from '@mui/icons-material/Delete';
import Switch from '@mui/material/Switch';
import useMediaQuery from '@mui/material/useMediaQuery';

import InfoIcon from '@mui/icons-material/Info';
import Tooltip from '@mui/material/Tooltip';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';

const SymptomSelection = ({ list_items, setListItems, setSelectedOptions, setSelectedProgression, setSelectedSymmetricity, setSelectedFamilyHistory, selected_progression, selected_symmetricity, selected_family_history, selectedOptions, handleProgressionToggle, handleSymmetricityToggle, familyHistoryToggle}) => {
  const isSmallScreen = useMediaQuery(theme => theme.breakpoints.down('sm'));

  async function getList() {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/symptoms?distinct_only=true`);
    const data = await response.json();
    return data;
  }

  const handleDelete = (optionToDelete) => () => {
    setSelectedOptions((options) => options.filter((option) => option.symptom_medical_name !== optionToDelete.symptom_medical_name));
  };

  React.useEffect(() => {
    getList().then(data => setListItems(data));
  }, []);
  React.useEffect(() => {
    setSelectedProgression(new Array(selectedOptions.length).fill('stable'));
  }, [selectedOptions]);
  React.useEffect(() => {
    setSelectedSymmetricity(new Array(selectedOptions.length).fill('na'));
  }, [selectedOptions]);
  React.useEffect(() => {
    setSelectedFamilyHistory(new Array(selectedOptions.length).fill(false));
  }, [selectedOptions]);

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
        filterOptions={(options, params) => {
          const filtered = options.filter((option) => {
            const tagsMatch = option.symptom_tags.some((tag) =>
              tag.toLowerCase().includes(params.inputValue.toLowerCase())
            );
            const bodyMatch = option.symptom_description
            .toLowerCase()
            .includes(params.inputValue.toLowerCase());
            const titleMatch = option.symptom_medical_name
            .toLowerCase()
            .includes(params.inputValue.toLowerCase());
            return tagsMatch || bodyMatch || titleMatch;
          });
          return filtered;
        }}
        renderOption={(props, option, { selected }) => {
          let srcPath = option.symptom_media_path.startsWith('http') ? option.symptom_media_path : `/media/${option.symptom_media_path}`;
          return (
          <Box {...props}>
            <Tooltip sx={{ maxWidth: 0.25 }} title={
                <Card>
                  <CardMedia
                    component="iframe" 
                    src={srcPath}
                    alt="tooltip_media"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h5" component="div">
                      {option.symptom_medical_name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {option.symptom_description}
                    </Typography>
                  </CardContent>
                </Card>
              }
              placement="right"
              arrow
              componentsProps={{
                tooltip: { sx: { bgcolor: 'transparent' , boxShadow: 'none',} },
              }}
              >
              <Button>
                <InfoIcon />
              </Button>
            </Tooltip>
            {option.symptom_medical_name}
          </Box>
        )}}
        renderInput={(params) => (
          <TextField {...params} label="Symptoms" placeholder="Type a symptom" />
        )}
        sx={{ width: '95%' }}
      />
      {/*Padded box for list of selections and attribute editing*/}
      <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '1em' }}>
        <List>
          <Grid container spacing={3}>
            <Grid item xs={isSmallScreen ? 6 : 3}><strong>Symptom</strong></Grid>
            <Grid item xs={isSmallScreen ? 6 : 3}><strong>Symptom Progression</strong></Grid>
            <Grid item xs={isSmallScreen ? 6 : 3}><strong>Symptom Symmetricity</strong></Grid>
            <Grid item xs={isSmallScreen ? 6 : 3}><strong>In Family History</strong></Grid>
          </Grid>
          {/*List contains multiselect selections*/}
          {selectedOptions.map((option, index) => (
          <ListItem key={index}>
            {/*1st item: delete button*/}
            <Grid container spacing={3}>
              <Grid item xs={isSmallScreen ? 6 : 3} container direction="row" alignItems="center">
                {/*1-A item: delete button*/}
                <IconButton edge="start" aria-label="delete" onClick={handleDelete(option)}>
                  <DeleteIcon />
                </IconButton>
                {/*1-B item: symptom text*/}
                <ListItemText primary={option.symptom_medical_name} />
              </Grid>
              {/*2nd item: box with progression choices group*/}
              <Grid item xs={isSmallScreen ? 6 : 3} flexDirection="row" alignItems="center">
                <ToggleButtonGroup 
                  value={selected_progression[index]}
                  exclusive
                  onChange={handleProgressionToggle}
                  orientation={isSmallScreen ? 'vertical' : 'horizontal'}
                  aria-label="progression choice"
                  sx={{ marginRight: '1em', flexWrap: 'wrap' }}>
                  <ToggleButton
                    value="stable"
                    onChange={handleProgressionToggle(index, 'stable')}
                    aria-label="stable"
                  >
                    Stable
                  </ToggleButton>
                  <ToggleButton
                    value="variable"
                    onChange={handleProgressionToggle(index, 'variable')}
                    aria-label="variable"
                  >
                    Variable
                  </ToggleButton>
                  <Select
                    value={selected_progression[index]}
                    onChange={handleProgressionToggle(index)}
                    inputProps={{ 'aria-label': 'progression choice'}}
                    label="PROGRESSION"
                  >
                    <MenuItem value={'slow_progressing'}>Slow Progressing</MenuItem>
                    <MenuItem value={'fast_progressing'}>Fast Progressing</MenuItem>
                  </Select>
                </ToggleButtonGroup>
              </Grid>
              {/*3rd item: box with symmetricity choices group*/}
              <Grid item xs={isSmallScreen ? 6 : 3} flexDirection="row" alignItems="center">
                <ToggleButtonGroup 
                  value={selected_symmetricity[index]}
                  onChange={handleSymmetricityToggle}
                  orientation={isSmallScreen ? 'vertical' : 'horizontal'}
                  aria-label="symmetricity"
                  sx={{ marginRight: '1em' , flexWrap: 'wrap' }}>
                  <ToggleButton
                    value="na"
                    onChange={handleSymmetricityToggle(index, 'na')}
                    aria-label="na"
                  >
                    NA
                  </ToggleButton>
                  <ToggleButton
                    value="unilateral"
                    onChange={handleSymmetricityToggle(index, 'unilateral')}
                    aria-label="unilateral"
                  >
                    1 Side
                  </ToggleButton>
                  <ToggleButton
                    value="bilateral"
                    onChange={handleSymmetricityToggle(index, 'bilateral')}
                    aria-label="bilateral"
                  >
                    2 Sides
                  </ToggleButton>
                </ToggleButtonGroup>
              </Grid>
              {/*4th item: switch for faimily history*/}
              <Grid item xs={isSmallScreen ? 6 : 3} flexDirection="row" alignItems="center">
                <Switch
                    checked={selected_family_history[index]}
                    onChange={() => familyHistoryToggle(index)}
                    name={`selected_family_history_${index}`}
                />
              </Grid>
            </Grid>
          </ListItem>
          ))}
        </List>
      </Box>
    </Box>
  );
};

export default SymptomSelection;
