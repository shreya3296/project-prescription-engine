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
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';

import SymptomMenu from '../SymptomMenu';


// const useStyles = makeStyles({
//     table: {
//       minWidth: 700,
//     },
//   });


const SubmitButton = ({onValueFromSubmitButton}) => {
    // const { classes } = props;

    console.log("================================== SubmitButton ======================================");


    // Component States


    // Setup Component
    useEffect(() => {

    }, []);

    const [state, setState] = useState({
        submitted: 0
    });

    const handleSubmit = () => {
        submitted = 1
        onValueFromSubmitButton(submitted)
    }

    const getState = () => (state)

    var submitted = 0

    return (
        // <div className={classes.root}>
        //     <main className={classes.main}>
                <Button 
                    variant="contained"
                    submitted = {0}
                    onClick={() => {
                        handleSubmit()
                    }}
                >
                    Diagnose
                </Button>

        //     </main>
        // </div>
    );
};

export default withStyles(styles)(SubmitButton);