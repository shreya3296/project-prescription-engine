import React, { useEffect, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
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


const SymptomTable = ({onValueFromSymptomTable}) => {

    console.log("================================== SymptomTable ======================================");


    // Component States
    

    // Setup Component
    useEffect(() => {

    }, []);

    // Handlers

    const [name, setName] = useState('');

    const handleSymptomEntry = (event) => {
        onValueFromSymptomTable(event.target.value)
    }
    return (

                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Symptoms</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableRow>
                            <TableCell align="center">
                                <TextField
                                    label = 'Symptom 1'
                                    variant = 'outlined'
                                    fullWidth
                                    onChange={(event) => (handleSymptomEntry(event))}
                                    />
                            </TableCell>
                        </TableRow>
                    </Table>
                </TableContainer>


    );
};

export default withStyles(styles)(SymptomTable);