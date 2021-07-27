
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';
import { makeStyles } from '@material-ui/core/styles';
import { DateTimePicker } from "@material-ui/pickers";
import { getDataOperationJob } from './store/dataOperationJobSlice'
import AppBar from '@material-ui/core/AppBar';
import Tab from '@material-ui/core/Tab';
import TabContext from '@material-ui/lab/TabContext';
import TabList from '@material-ui/lab/TabList';
import TabPanel from '@material-ui/lab/TabPanel';
import DataOperationJobExecutions from '../executions/DataOperationJobExecutions';

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
}));

function DataOperationJobData() {

	const classes = useStyles();
	const dispatch = useDispatch();
	const formClasses = filterFormStyles();

	const [values, setValues] = React.useState({
		id: 0,
		jobId: 0,
		dataOperationId: null,
		dataOperationName: "",
		cron: "",
		startDate: new Date(),
		endDate: new Date(),
		nextRunTime: new Date(),
		creationDate: new Date(),
		lastUpdatedDate: new Date(),
		isDeleted: 0,
	});

	const handleChange = (prop) => (event) => {
		setValues({ ...values, [prop]: event.target.value });
	};


	const routeParams = useParams();

	const operationJob = useSelector(({ dataOperationJobApp }) => {
		return dataOperationJobApp.dataOperationJob.entities[routeParams.id]
	});

	useEffect(() => {
		dispatch(getDataOperationJob(routeParams));
	}, [dispatch, routeParams]);

	useEffect(() => {
		if (operationJob && operationJob != null) {
			let operationJobData = { ...operationJob }

			setValues(operationJobData);
		}
	}, [operationJob]);


	const [tabValue, setTabValue] = React.useState('1');
	const handleTabChange = (event, newValue) => {

		setTabValue(newValue);
	};

	const checkValue = value => value ? value : ''
	return (
		<div className={formClasses.root}
			style={{ padding: '15px 40px 15px 40px' }}
		>
			<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>

			<form className={classes.root} noValidate autoComplete="off" style={{ padding: ' 0 0 15px 0' }}>
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="definitionId" label="Id" value={checkValue(values.id)}
							disabled
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}} onChange={handleChange('definitionId')} />
					</Grid>
					<Grid item xs>
						<TextField id="definitionId" label="Job Id" value={checkValue(values.jobId)}
							disabled
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}} onChange={handleChange('definitionId')} />
					</Grid>
					<Grid item xs>
						<TextField id="name" label="Data Operation Name" value={checkValue(values.dataOperationId + '-' + values.dataOperationName)}
							disabled

							fullWidth={true} onChange={handleChange('name')} />
					</Grid>
					<Grid item xs>
						<DateTimePicker
							disabled
							fullWidth={true}
							label="Creation Date"
							inputVariant="outlined"
							value={checkValue(values.creationDate)}
							onChange={handleChange('creationDate')}
							format="DD/MM/yyyy HH:mm:sss a"
						/>
					</Grid>
				</Grid>

				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="name" label="Cron" value={checkValue(values.cron)}
							disabled

							fullWidth={true} onChange={handleChange('name')} />
					</Grid>

					<Grid item xs>
						<DateTimePicker
							disabled
							fullWidth={true}
							label="Start Date"
							inputVariant="outlined"
							value={values.startDate}
							onChange={handleChange('startDate')}
							format="DD/MM/yyyy HH:mm:sss a"
						/>
					</Grid>
					<Grid item xs>
						<DateTimePicker
							disabled
							fullWidth={true}
							label="End Date"
							inputVariant="outlined"
							value={values.endDate}
							onChange={handleChange('startDate')}
							format="DD/MM/yyyy HH:mm:sss a"
						/>
					</Grid>
					<Grid item xs>
						<DateTimePicker
							disabled
							fullWidth={true}
							label="Next Run Time"
							inputVariant="outlined"
							value={values.nextRunTime}
							onChange={handleChange('startDate')}
							format="DD/MM/yyyy HH:mm:sss a"
						/>
					</Grid>
				</Grid>
				<Grid container spacing={3}>
					<Grid item xs={3}>
						<TextField id="isDeleted" label="Is Deleted" value={values.isDeleted}
							disabled
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}} onChange={handleChange('name')} />
					</Grid>
				</Grid>
			</form>

			<TabContext value={tabValue}>
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
						values.dataOperationId && values.dataOperationId !== null && values.dataOperationId !== 0 ? (
							<DataOperationJobExecutions HasHeader={false} DataOperationId={values.dataOperationId} />
						) :
							("")
					}
				</TabPanel>
			</TabContext>
		</div>
	);
}

export default withRouter(DataOperationJobData);
