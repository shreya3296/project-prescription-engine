import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TextField from '@material-ui/core/TextField';
import Alert from '@material-ui/lab/Alert';



import DataService from "../../services/DataService";
import styles from './styles';
import SymptomTable from '../SymptomTable';
import DemographicsTable from '../DemographicsTable';
import SubmitButton from '../SubmitButton';


const SymptomMenu = (props) => {
    const { classes } = props;

    console.log("================================== SymptomMenu ======================================");


    // Component States
    const [contentList, setContentList] = useState([]);

    // Setup Component
    useEffect(() => {

    }, []);

    // Handlers

    const [valueFromSubmitButton, setValueFromSubmitButton] = useState('');
    const [valueFromSymptomTable, setValueFromSymptomTable] = useState('');
    const [valuesFromDemographicsTable, setValuesFromDemographicsTable] = useState('');
    // const [isVisible, setIsVisible] = useState('false');


    const getPercentage = (num) => (
        `${(num*100).toFixed(1)}%`
    )
    const apiURL = "https://api-service-2-pdxll6t53q-uc.a.run.app/use/"
    var patientInfo = {
        age: null,
        sex: null,
        symptoms: null,
    }

    const getRequestData = (dict) => ({
        input_message: {
            symptoms: dict.symptoms,
            age: dict.age,
            gender: dict.sex,
        }
    })

    const createRequest = (data) => ({
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
    })

    const checkBadUserInput = () => {
        let nullElements = getKeysWithNullValues(patientInfo)
        console.log("patientInfo",patientInfo)
        console.log("nullElements",nullElements)
        if (nullElements.length > 0) {
            let alertText = 'Please enter the ' + nullElements.join(", ")
            alert(alertText)
            return false
        }
        return true
    }

    const getKeysWithNullValues = (obj) => (
        Object.keys(obj).filter(key => obj[key] === null)
    )

    async function sendToAPI(request) { 
        // TODO Error catching
        const response = await fetch(apiURL, request);
        const diagnosisData = response.json();
        console.log(diagnosisData);
    }

    var response = null;
    // var diagnosisData = null; // should start null
    var diagnosisData = {"prediction":[["J45","Test",0.4382490813732147],["J38.5","Test",0.3069225251674652],["a15","Test",0.22649161517620087],["j44.1","Test",0.017185017466545105],["J47","Test",0.0060112024657428265]]}
    // Callback function to receive values from the SubmitButton
    const handleValueFromSubmitButton = (value) => {
        console.log(value)
        if (!checkBadUserInput()) return;
        setValueFromSubmitButton(value);
        // let data = getRequestData(patientInfo)
        // let request = createRequest(data)
        // response = sendToAPI(request)
        // diagnosisData = response
        // setIsVisible(value);
    };

    // Callback function to receive values from the SymptomTable
    const handleValueFromSymptomTable = (value) => {
        console.log(value)
        setValueFromSymptomTable(value);
        if (value !== null && typeof value === 'number' && Number.isInteger(value)) {
            patientInfo["age"] = value;
        } else {
            patientInfo["sex"] = value;
        }
        console.log("patientInfo", patientInfo)
    };

    // Callback function to receive values from the DemographicsTable
    const handleValuesFromDemographicsTable = (value) => {
        console.log(value)
        setValuesFromDemographicsTable(value);
        patientInfo["symptoms"] = value;
        console.log("patientInfo", patientInfo)
    };

    // TODO: If submit pressed, wait for response then show diagnosis and prescription

    return (
        <div className={classes.root}>
            <main className={classes.main}>
                <Container maxWidth={false} className={classes.container}>
                    <Grid 
                        container 
                        direction="column"
                        justifyContent="center"
                        alignItems="stretch"
                    >
                        <Grid>
                            <Typography variant="h5" gutterBottom>Demographic Information</Typography>
                            <DemographicsTable onValuesFromDemographicstable={handleValuesFromDemographicsTable}/>
                        </Grid>
                        <Grid>
                            <Typography variant="h5" gutterBottom>Symptoms</Typography>
                            <SymptomTable onValueFromSymptomTable={handleValueFromSymptomTable}/>
                        </Grid>
                        <Grid>
                            <SubmitButton onValueFromSubmitButton={handleValueFromSubmitButton}/>
                        </Grid>
                        <Grid>
                        {diagnosisData && <TableContainer component={Paper}>
                            <Typography variant="h5" gutterBottom>Diagnoses</Typography>
                            <Table>
                               <TableHead>
                                    <TableRow>
                                        <TableCell>Diagnosis Code</TableCell>
                                        <TableCell>Description</TableCell>
                                        <TableCell>Confidence</TableCell>
                                        <TableCell>Prescription</TableCell>
                                    </TableRow>
                                </TableHead>
                                
                                {diagnosisData ? 
                                diagnosisData['prediction']
                                    .sort((a,b) => b[2] - a[2])
                                    .map((value) => (
                                <TableRow>
                                    <TableCell>{value[0]}</TableCell>
                                    <TableCell>{value[1]}</TableCell>
                                    <TableCell>{getPercentage(value[2])}</TableCell>
                                    <TableCell><Button variant="contained">GET</Button></TableCell>
                                </TableRow>
                                )) : null}
                                <TableRow>
                                </TableRow>
                            </Table>
                        </TableContainer>
                        }
                        {diagnosisData && <Alert severity="warning">This is a project for research purposes only and should never be used as medical advice. If you have any symptoms, please consult with a medical professional.</Alert>}
                        </Grid>
                        {/* TODO: Alert message that says "Please fill in..." */}
                    </Grid>
                </Container>
            </main>
        </div>
    );
};

export default withStyles(styles)(SymptomMenu);