
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';
import { makeStyles } from '@material-ui/core/styles';
import { DateTimePicker } from "@material-ui/pickers";
import AppBar from '@material-ui/core/AppBar';
import Tab from '@material-ui/core/Tab';
import TabContext from '@material-ui/lab/TabContext';
import TabList from '@material-ui/lab/TabList';
import TabPanel from '@material-ui/lab/TabPanel';
import { getDataOperationJobExecution } from './store/dataOperationJobExecutionSlice';
import { getStatusName, selectStatusName } from './store/statusNameSlice';
import DataOperationJobExecutionIntegrationsData from './DataOperationJobExecutionIntegrationsData'
import DataOperationJobExecutionLogsData from './DataOperationJobExecutionLogsData'

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
function DataOperationJobExecutionContent(props) {

	const classes = useStyles();
	const dispatch = useDispatch();
	const formClasses = filterFormStyles();
	const [values, setValues] = React.useState({
		id: 0,
		jobId: 0,
		dataOperationId: "",
		dataOperationName: "",
		scheduleInfo: {},
		statusId: 0,
		statusDescription: "",
		log: "",
		sourceDataCount: 0,
		affectedRowCount: 0,
		startDate: new Date(),
		endDate: new Date(),
	});

	const [status, setStatus] = React.useState(null);
	const selectStatusNames = useSelector(selectStatusName);

	const routeParams = useParams();

	const operationJobExecution = useSelector(({ dataOperationJobExecutionApp }) => {
		return dataOperationJobExecutionApp.dataOperationJobExecution.entities[routeParams.id]
	});

	useEffect(() => {
		dispatch(getDataOperationJobExecution(routeParams));
		dispatch(getStatusName(routeParams));
	}, [dispatch, routeParams]);

	useEffect(() => {
		if (operationJobExecution && operationJobExecution != null && selectStatusNames && selectStatusNames != null) {
			let operationJobExecutionData = { ...operationJobExecution }

			setValues(operationJobExecutionData);
			let status = selectStatusNames.filter(name => name.id === operationJobExecutionData.statusId)
			if (status != null && status.length > 0) {
				setStatus(status[0].name)
			}
		}
	}, [operationJobExecution, selectStatusNames]);


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
					<Grid item xs={2}>
						<TextField
							id="definitionId"
							label="Id"
							value={checkValue(values.id)}
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}}
							InputProps={{
								readOnly: true,
							}}
						/>
					</Grid>

					<Grid item xs={1}>
						<TextField id="definitionId" label="Job Id" value={checkValue(values.jobId)}
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}}
							InputProps={{
								readOnly: true,
							}}
						/>
					</Grid>

					<Grid item xs={3}>
						<TextField id="definitionId" label="Job Id" value={checkValue(status)}
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							InputProps={{
								readOnly: true,
							}}
						/>
					</Grid>
					<Grid item xs>
						<TextField
							id="name"
							label="Data Operation"
							value={checkValue(values.dataOperationId) + '-' + checkValue(values.dataOperationName)}
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							InputProps={{
								readOnly: true,
							}}
						/>
					</Grid>
					<Grid item xs>
						<TextField id="name" label="Schedule Info"
							value={checkValue(values.scheduleInfo.cron) + '(' + checkValue(values.scheduleInfo.startDate) + '-' + checkValue(values.scheduleInfo.endDate) + ')'}
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							InputProps={{
								readOnly: true,
							}}
						/>
					</Grid>

				</Grid>

				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="sourceDataCount" label="Source Data Count" value={values.sourceDataCount}
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}}
							InputProps={{
								readOnly: true,
							}}
						/>
					</Grid>
					<Grid item xs>
						<TextField id="affectedRowCount" label="Affected Row Count" value={values.affectedRowCount}
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}}
							InputProps={{
								readOnly: true,
							}}
						/>
					</Grid>
					<Grid item xs>
						<DateTimePicker
							readOnly
							fullWidth={true}
							label="Start Date"
							inputVariant="outlined"
							value={values.startDate}
							format="DD/MM/yyyy HH:mm:sss a"
							InputLabelProps={{
								shrink: true,
							}}
						/>
					</Grid>
					<Grid item xs>
						<DateTimePicker
							readOnly
							fullWidth={true}
							label="End Date"
							inputVariant="outlined"
							value={values.endDate}
							format="DD/MM/yyyy HH:mm:sss a"
							InputLabelProps={{
								shrink: true,
							}}
						/>
					</Grid>
				</Grid>
			</form>

			<TabContext value={tabValue}>
				<AppBar position="static">
					<TabList onChange={handleTabChange} aria-label="simple tabs example" >
						<Tab label="Integrations" value="1" />
						<Tab label="Logs" value="2" />
					</TabList>
				</AppBar>
				<TabPanel value="1">
					{
						values.id && values.id !== null && values.id !== 0 ? (
							<DataOperationJobExecutionIntegrationsData ExecutionId={values.id} />
						) :
							("")
					}
				</TabPanel>
				<TabPanel value="2">
					{
						values.id && values.id !== null && values.id !== 0 ? (
							<DataOperationJobExecutionLogsData ExecutionId={values.id} />
						) :
							("")
					}
				</TabPanel>
			</TabContext>
		</div>
	);
}

export default withRouter(DataOperationJobExecutionContent);
