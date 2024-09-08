import React, { useEffect, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import FormControl from '@material-ui/core/FormControl';
import FormHelperText from '@material-ui/core/FormHelperText';
import InputLabel from '@material-ui/core/InputLabel';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Checkbox from '@material-ui/core/Checkbox';
import Divider from '@material-ui/core/Divider';
import { Link } from 'react-router-dom';
import { Icon } from '@material-ui/core';
import styles from './styles';
import Paper from '@material-ui/core/Paper';
import TableContainer from '@material-ui/core/TableContainer';
import { makeStyles } from '@material-ui/core/styles';

// const useStyles = makeStyles({
//     table: {
//       minWidth: 700,
//     },
//   });


const DemographicsTable = ({onValuesFromDemographicstable}) => {

    console.log("================================== TOC ======================================");


    // Component States


    // Setup Component
    useEffect(() => {

    }, []);

    // Handlers


    // const styleClasses = useStyles();
    const [state, setState] = useState({
        male: false,
        female: false,
        age: null
    });
    
    
    const handleChange = (event) => {
        setState({
            ...{                
                male: false,
                female: false,
          },
          [event.target.name]: event.target.checked,
        });
        onValuesFromDemographicstable(event.target.name)
      };
    const { male, female } = state;

    const handleAgeChange = (event) => {
        setState({
            ...state,
            age: event.target.value
        })
        onValuesFromDemographicstable(event.target.value)
    };

    const ageOptions = Array.from(Array(95), (x,i) => x = i+5)


    return (

                <TableContainer component={Paper}>

                    <Table>
                        {/* TODO: Make Age and sex required? */}

                        <TableHead>
                            <TableRow>
                                <TableCell>Age</TableCell>
                                <TableCell>Sex</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableRow>
                            <TableCell></TableCell>
                            <TableCell>Male</TableCell>
                            <TableCell>Female</TableCell>
                        </TableRow>
                        <TableRow>
                            <FormControl fullWidth>
                                <InputLabel id="demo-simple-select-label">Age</InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    // value={age}
                                    label="Age *"
                                    onChange={handleAgeChange}
                                >

                                    {ageOptions.map((value) => (
                                        <MenuItem key = {value} value = {value}>
                                            {value}
                                        </MenuItem>
                                        
                                    ))}
                                </Select>
                            </FormControl>
                            <TableCell align="center">
                                <Checkbox checked={male} onChange={handleChange} name="male"/>
                            </TableCell>
                            <TableCell align="center">
                                <Checkbox checked={female} onChange={handleChange} name="female"/>
                            </TableCell>
                            {/* <FormHelperText>Required</FormHelperText> */}
                        </TableRow>
                    </Table>
                </TableContainer>


    );
};

export default withStyles(styles)(DemographicsTable);