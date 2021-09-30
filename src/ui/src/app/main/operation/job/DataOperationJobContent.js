
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import { DateTimePicker } from "@material-ui/pickers";
import AppBar from '@material-ui/core/AppBar';
import Tab from '@material-ui/core/Tab';
import TabContext from '@material-ui/lab/TabContext';
import TabList from '@material-ui/lab/TabList';
import TabPanel from '@material-ui/lab/TabPanel';
import Box from '@material-ui/core/Box';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import RadioGroup from '@material-ui/core/RadioGroup';
import Radio from '@material-ui/core/Radio';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { getOperationJob, clearDataOperationJob, postScheduleCronJob, deleteScheduleCronJob, postScheduleJob, deleteScheduleJob } from './store/dataOperationJobSlice'
import DataOperationJobExecutions from '../executions/DataOperationJobExecutions';
import { getDataOperationName, selectDataOperationName } from './store/dataOperationNameSlice';
import { toast } from 'react-toastify';

const useStyles = makeStyles(theme => ({
	root: {
		"& .MuiTextField-root": {
			margin: theme.spacing(1)
		}
	},
	textarea: {
		resize: "both",
	},
	textareamargin: {
		margin: "10px 0 0 5px"
	},
	divider: {
		margin: theme.spacing(2, 0),
	},
	button: {
		margin: theme.spacing(1),
		"white-space": "nowrap",
	},
	box: {
		display: "flex",
	},
	bottomRightBox: {
		justifyContent: "flex-end",
		alignItems: "flex-end"
	},
	centerBox: {
		justifyContent: "center",
		alignItems: "center"
	},
	topLeftBox: {
		justifyContent: "flex-start",
		alignItems: "flex-start"
	}
}));
function DataOperationJobContent() {

	const classes = useStyles();
	const dispatch = useDispatch();

	const filterOptions = createFilterOptions({
		matchFrom: 'any',
		stringify: option => {
			return option.name
		},
	});
	const initialState = {
		id: 0,
		jobId: 0,
		dataOperation: null,
		dataOperationId: null,
		dataOperationName: "",
		type: "Execute",
		cron: "",
		startDate: null,
		endDate: null,
		nextRunTime: null,
		creationDate: null,
		isDeleted: 0,
	}
	const [values, setValues] = React.useState(initialState);
	const [disabilityStatus, setDisabilityStatus] = React.useState({});
	const [readonlyStatus, setReadonlyStatus] = React.useState({});

	const handleChangeValue = (event, prop, value) => {
		setValues({ ...values, [prop]: value });
	};

	const handleChange = (prop) => (event) => {
		handleChangeValue(event, prop, event.target.type === 'number' ? (parseInt(event.target.value) || 0) : event.target.value)
	};

	const routeParams = useParams();

	const operationJob = useSelector(({ dataOperationJobApp }) => {
		return dataOperationJobApp.dataOperationJob.data
	});
	const selectDataOperationNames = useSelector(selectDataOperationName);

	useEffect(() => {
		dispatch(getDataOperationName(routeParams));
		if (routeParams.id && routeParams.id != null) {
			dispatch(getOperationJob(routeParams));
		}
		else {
			dispatch(clearDataOperationJob(routeParams));
		}
	}, [dispatch, routeParams]);

	const initializeValues = () => {
		if (operationJob && operationJob != null && Object.keys(operationJob).length !== 0) {

			let operationJobData = { ...operationJob }
			let operation = selectDataOperationNames.filter(name => name.id === parseInt(operationJobData.dataOperationId))
			if (operation !== null && operation?.length > 0) {
				operationJobData.dataOperation = operation[0]
			}
			if (operationJobData.cron && operationJobData.cron !== null && operationJobData.cron !== '') {
				operationJobData.type = 'Cron'
			}
			else if (operationJobData.startDate && operationJobData.startDate !== null) {
				operationJobData.type = 'Schedule'
			}
			else {
				operationJobData.type = 'Execute'
			}
			setValues(operationJobData);
		}
		else {
			setValues(initialState);
		}
	}
	useEffect(() => {
		if (operationJob && operationJob != null && selectDataOperationNames && selectDataOperationNames != null) {
			initializeValues()

			setDisabilityStatus({
				id: true,
				jobId: true,
				dataOperation: ((operationJob.id && operationJob.id !== null) || operationJob.isDeleted === 1) ? true : false,
				dataOperationId: true,
				dataOperationName: true,
				type: ((operationJob.id && operationJob.id !== null) || operationJob.isDeleted === 1) ? true : false,
				cron: ((operationJob.id && operationJob.id !== null) || operationJob.isDeleted === 1) ? true : false,
				startDate: ((operationJob.id && operationJob.id !== null) || operationJob.isDeleted === 1) ? true : false,
				endDate: ((operationJob.id && operationJob.id !== null) || operationJob.isDeleted === 1) ? true : false,
				nextRunTime: true,
				creationDate: true,
				lastUpdatedDate: true,
				isDeleted: true
			})
			setReadonlyStatus({
				id: true,
				jobId: true,
				dataOperation: ((operationJob.id && operationJob.id !== null)) ? true : false,
				dataOperationId: true,
				dataOperationName: true,
				type: ((operationJob.id && operationJob.id !== null)) ? true : false,
				cron: ((operationJob.id && operationJob.id !== null)) ? true : false,
				startDate: ((operationJob.id && operationJob.id !== null)) ? true : false,
				endDate: ((operationJob.id && operationJob.id !== null)) ? true : false,
				nextRunTime: true,
				creationDate: true,
				lastUpdatedDate: true,
				isDeleted: true
			})
		}
	}, [operationJob, selectDataOperationNames]);


	const [tabValue, setTabValue] = React.useState('1');
	const handleTabChange = (event, newValue) => {

		setTabValue(newValue);
	};



	const save = event => {
		if (values.dataOperation === undefined || values.dataOperation === null || values.dataOperation.name === undefined || values.dataOperation.name  === '') {
			toast.warn('Data Operation required', { position: toast.POSITION.BOTTOM_RIGHT })
			return
		}
		switch (values.type) {
			case "Execute":
				{
					let request = {
						OperationName: values.dataOperation.name
					}
					dispatch(postScheduleJob(request));
				}
				break;
			case "Schedule":
				{
					let request = {
						OperationName: values.dataOperation.name,
						RunDate: values.startDate
					}
					dispatch(postScheduleJob(request));
				}
				break;
			case "Cron":
				{
					if (values.cron === undefined || values.cron === null || values.cron === '') {
						toast.warn('Cron required', { position: toast.POSITION.BOTTOM_RIGHT })
						return
					}
					if (values.startDate && values.endDate) {
						if (values.startDate > values.endDate) {
							toast.warn('End Date must bigger than Start Date', { position: toast.POSITION.BOTTOM_RIGHT })
							return
						}
					}
					let request = {
						OperationName: values.dataOperation.name,
						Cron: values.cron
					}
					
					if (values.startDate !== undefined && values.startDate !== null && values.startDate !== '') {
						request['StartDate']=values.startDate
					}
					if (values.endDate !== undefined && values.endDate !== null && values.endDate !== '') {
						request['EndDate']=values.endDate
					}
					dispatch(postScheduleCronJob(request));
				}
				break;
			default:
				break;
		}
	};

	const clear = event => {
		initializeValues()
	};

	const deleteAction = () => {
		switch (values.type) {
			case "Execute":
				{
					let request = {
						Id: values.id
					}
					dispatch(deleteScheduleJob(request));
				}
				break;
			case "Schedule":
				{
					let request = {
						Id: values.id
					}
					dispatch(deleteScheduleJob(request));
				}
				break;
			case "Cron":
				{
					let request = {
						OperationName: values.dataOperation.name
					}
					dispatch(deleteScheduleCronJob(request));
				}
				break;
			default:
				break;
		}
	}
	const checkValue = value => value ? value : ''
	return (
		<Box>
			<form className={classes.root} noValidate autoComplete="off" style={{ padding: ' 0 0 15px 0' }}>
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField
							id="id"
							label="Id"
							type="number"
							variant="outlined"
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							disabled={disabilityStatus.id}
							readOnly={readonlyStatus.id}
							value={checkValue(values.id)}
							onChange={handleChange('definitionId')}
						/>
					</Grid>
					<Grid item xs>
						<Autocomplete
							id="country-select-demo"
							style={{ width: '100%' }}
							fullWidth={true}
							autoHighlight
							clearOnEscape
							openOnFocus
							options={selectDataOperationNames}
							classes={{
								option: classes.option,
							}}
							filterOptions={filterOptions}
							getOptionLabel={(option) => option?.name}
							renderOption={(option) => (
								<React.Fragment>
									<span>{option?.name}</span>
								</React.Fragment>
							)}
							renderInput={(params) => (
								<TextField
									{...params}
									label="Data Operation"
									variant="outlined"
									inputProps={{
										...params.inputProps,
										autoComplete: 'new-password', // disable autocomplete and autofill
									}}
								/>
							)}
							disabled={disabilityStatus.dataOperation}
							readOnly={readonlyStatus.dataOperation}
							value={values.dataOperation}
							onChange={(event, newValue) => {
								handleChangeValue(event, 'dataOperation', newValue);
							}}
						/>
					</Grid>
					<Grid item xs>
						<Box style={{ width: '100%' }}>
							<Grid container spacing={1}>
								<Grid item xs>
									<DateTimePicker
										label="Creation Date"
										inputVariant="outlined"
										format="DD/MM/yyyy HH:mm:sss a"
										fullWidth={true}
										disabled={disabilityStatus.creationDate}
										readOnly={readonlyStatus.creationDate}
										value={values.creationDate}
									/>
								</Grid>
								<Grid item xs={4}>
									<TextField
										id="isDeleted"
										label="Is Deleted"
										type="number"
										variant="outlined"
										fullWidth={true}
										InputLabelProps={{
											shrink: true,
										}}
										disabled={disabilityStatus.isDeleted}
										readOnly={readonlyStatus.isDeleted}
										value={values.isDeleted}
									/>
								</Grid>
							</Grid>
						</Box>
					</Grid>
					<Grid item xs>
						<DateTimePicker
							label="Next Run Time"
							inputVariant="outlined"
							format="DD/MM/yyyy HH:mm:sss a"
							fullWidth={true}
							disabled={disabilityStatus.nextRunTime}
							readOnly={readonlyStatus.nextRunTime}
							value={values.nextRunTime}
						/>
					</Grid>
				</Grid>
				<Grid container spacing={3}>
					<Grid item xs>
						<RadioGroup
							row aria-label="position"
							name="position"
							label="position"
							style={{ margin: '0 0 0 5px' }}
							value={values.type}
							onChange={handleChange('type')}>
							<FormControlLabel value="Execute" control={<Radio color="primary" />} label="Execute" disabled={disabilityStatus.type} style={{ padding: '0 0 0 5px' }} />
							<FormControlLabel value="Schedule" control={<Radio color="primary" />} label="Schedule" disabled={disabilityStatus.type} />
							<FormControlLabel value="Cron" control={<Radio color="primary" />} label="Cron" disabled={disabilityStatus.type} />
						</RadioGroup>
					</Grid>
				</Grid>

				{
					values.type !== 'Execute' ?
						(
							<Grid container spacing={3}>
								{
									values.type === 'Cron' ?
										(
											<Grid item xs>
												<TextField
													id="name"
													label="Cron"
													variant="outlined"
													fullWidth={true}
													InputLabelProps={{
														shrink: true,
													}}
													disabled={disabilityStatus.cron}
													readOnly={readonlyStatus.cron}
													value={checkValue(values.cron)}
													onChange={handleChange('cron')}
												/>
											</Grid>
										) : ('')
								}

								{
									values.type !== 'Execute' ?
										(
											<Grid item xs>
												<DateTimePicker
													clearable={values.type === 'Cron'}
													label={values.type === 'Cron' ? "Start Date" : "Run Date"}
													inputVariant="outlined"
													format="DD/MM/yyyy HH:mm:sss a"
													fullWidth={true}
													InputLabelProps={{
														shrink: true,
													}}
													renderInput={(props) => <TextField {...props} />}
													disabled={disabilityStatus.startDate}
													readOnly={readonlyStatus.startDate}
													value={values.startDate}
													onChange={(value) => {
														handleChangeValue(null, 'startDate', value);
													}}
												/>
											</Grid>
										) : ('')
								}
								{
									values.type === 'Cron' ?
										(
											<Grid item xs>
												<DateTimePicker
													clearable
													label="End Date"
													inputVariant="outlined"
													format="DD/MM/yyyy HH:mm:sss a"
													fullWidth={true}
													InputLabelProps={{
														shrink: true,
													}}
													renderInput={(props) => <TextField {...props} />}
													disabled={disabilityStatus.endDate}
													readOnly={readonlyStatus.endDate}
													value={values.endDate}
													onChange={(value) => {
														handleChangeValue(null, 'endDate', value);
													}}
												/>
											</Grid>
										) : ('')
								}
							</Grid>
						) : ('')
				}
				{
					values.isDeleted !== 1 ?
						(
							<Box
								component="span"
								m={1} //margin
								className={`${classes.bottomRightBox} ${classes.box}`}
							>
								<ButtonGroup aria-label="outlined primary button group">
									{
										values.id && values.id != null ? (
											<Button
												variant="contained"
												color="default"
												size="large"
												className={classes.button}
												startIcon={<Icon >delete</Icon>}
												onClick={deleteAction}
											>
												Delete
											</Button>
										) : ("")
									}
									{
										!(values.id && values.id !== null && values.id !== 0) ?
											(
												<Button
													variant="contained"
													color="secondary"
													size="large"
													className={classes.button}
													startIcon={<Icon >clear</Icon>}
													onClick={clear}
												>
													Clear
												</Button>
											) : ("")
									}
									{
										!(values.id && values.id !== null && values.id !== 0) ?
											(
												<Button
													variant="contained"
													color="primary"
													size="large"
													className={classes.button}
													startIcon={<Icon >save</Icon>}
													onClick={save}
												>
													Save
												</Button>
											) : ("")
									}
								</ButtonGroup>
							</Box>
						) : ("")
				}
			</form>

			{
				values.id && values.id !== null && values.id !== 0 ?
					(
						< TabContext value={tabValue}>
							<AppBar position="static">
								<TabList onChange={handleTabChange} aria-label="simple tabs example" >
									<Tab label="Executions" value="1" />
									{/* <Tab label="Definitions" value="2" />
						<Tab label="Jobs" value="3" />
						<Tab label="Executions" value="4" /> */}
								</TabList>
							</AppBar>
							<TabPanel value="1">
								{
									values.id && values.id !== null && values.id !== 0 ? (
										<DataOperationJobExecutions HasHeader={false} DataOperationJobId={values.id} />
									) :
										("")
								}
							</TabPanel>
						</TabContext>
					) : ("")
			}
		</Box >
	);
}

export default withRouter(DataOperationJobContent);
