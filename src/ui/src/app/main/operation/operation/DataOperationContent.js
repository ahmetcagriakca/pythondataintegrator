import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import Icon from '@material-ui/core/Icon';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import { DateTimePicker } from "@material-ui/pickers";
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Tab from '@material-ui/core/Tab';
import TabContext from '@material-ui/lab/TabContext';
import TabList from '@material-ui/lab/TabList';
import TabPanel from '@material-ui/lab/TabPanel';
import { getOperation, postOperation, deleteOperation, clearOperation } from './store/dataOperationSlice';
import { getConnectionName } from './store/connectionNameSlice';
import DataOperationJobExecutions from '../executions/DataOperationJobExecutions';
import DataOperationJobs from '../jobs/DataOperationJobs';
import DataOperationContactsData from './contacts/DataOperationContactsData';
import DataOperationIntegrationsData from './DataOperationIntegrationsData';
import { toast } from 'react-toastify';

import DataOperationJsonContent from './DataOperationJsonContent';

const useStyles = makeStyles(theme => ({
	root: {
		"& .MuiTextField-root": {
			margin: theme.spacing(1)
		}
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
	},
	appBar: {
		position: 'relative',
	},
	title: {
		marginLeft: theme.spacing(2),
		flex: 1,
	},
}));

function DataOperationContent() {
	const classes = useStyles();
	const dispatch = useDispatch();
	const routeParams = useParams();
	const checkValue = value => value ? value : ''

	const [tabValue, setTabValue] = React.useState('1');
	const [disabilityStatus, setDisabilityStatus] = React.useState({});
	const [readonlyStatus, setReadonlyStatus] = React.useState({});
	const operation = useSelector(({ dataOperationApp }) => {
		return dataOperationApp.dataOperation.data
	});

	const [values, setValues] = React.useState({
		id: null,
		name: '',
		definitionId: 0,
		version: 0,
		contacts: null,
		integrations: null,
		creationDate: new Date(),
		isDeleted: true,
	});

	useEffect(() => {
		dispatch(getConnectionName(routeParams));
		if (routeParams.id && routeParams.id != null) {
			dispatch(getOperation(routeParams));
		}
		else {

			dispatch(clearOperation(routeParams));
		}
	}, [dispatch, routeParams]);
	const initializeValues = () => {
		if (operation && operation != null) {

			let operationData = {
				id: operation.id?operation.id:null,
				name: operation.name?operation.name:'',
				definitionId: operation.definitionId?operation.definitionId:0,
				version: operation.version?operation.version:0,
				contacts: operation.contacts?operation.contacts:null,
				integrations: operation.integrations?operation.integrations:null,
				creationDate: operation.creationDate?operation.creationDate:new Date(),
				isDeleted: operation.isDeleted?operation.isDeleted:0,
			}
			if (!(operationData.contacts && operationData.concats?.length !== 0)) {
				operationData.contacts = []
			}
			if (!(operationData.integrations && operationData.integrations?.length !== 0)) {
				operationData.integrations = []
			}
			setValues(operationData);
		}
	}
	useEffect(() => {
		if (operation && operation != null) {
			initializeValues()
			setDisabilityStatus({
				id: true,
				name: ((operation.id && operation.id !== null) || operation.isDeleted === 1) ? true : false,
				definitionId: true,
				version: true,
				creationDate: true,
				isDeleted: true,
			})
			setReadonlyStatus({
				id: true,
				name: ((operation.id && operation.id !== null)) ? true : false,
				definitionId: true,
				version: true,
				creationDate: true,
				isDeleted: true,
			})
		}
	}, [operation]);

	const handleChangeValue = (event, prop, value) => {
		setValues({ ...values, [prop]: value });
	};

	const handleChange = (prop) => (event) => {
		handleChangeValue(event, prop, event.target.type === 'number' ? (parseInt(event.target.value) || 0) : event.target.value)
	};

	const handleTabChange = (event, newValue) => {
		setTabValue(newValue);
	};

	const createOperationJson = (operationData, validate) => {
		let hasError = false
		let contacts = []
		for (var i = 0; i < operationData?.contacts?.length; i++) {
			contacts = contacts.concat({ Email: operationData.contacts[i].email })
		}

		let operationIntegrations = []
		for (var j = 0; j < operationData?.integrations?.length; j++) {
			let dataOperationIntegration = operationData.integrations[j]
			let dataIntegration = dataOperationIntegration.integration
			let sourceColumns = []
			let targetColumns = []

			if (
				dataIntegration?.sourceConnection &&
				dataIntegration?.sourceConnection != null &&
				dataIntegration?.sourceConnection?.connection?.name != null &&
				dataIntegration?.targetConnection &&
				dataIntegration?.targetConnection != null &&
				dataIntegration?.targetConnection?.connection?.name != null) {
				for (var k = 0; k < dataIntegration.columns.length; k++) {
					sourceColumns = sourceColumns.concat(dataIntegration.columns[k].sourceColumnName)
					targetColumns = targetColumns.concat(dataIntegration.columns[k].targetColumnName)
				}
			}
			let sourceConnections = null
			if (
				dataIntegration?.sourceConnection &&
				dataIntegration?.sourceConnection != null &&
				dataIntegration?.sourceConnection?.connection?.name != null
			) {
				sourceConnections = {
					ConnectionName: dataIntegration.sourceConnection.connection.name
				}
				if (dataIntegration?.targetConnection?.connection?.connectionTypeId === 1) {
					let database = {
						Schema: dataIntegration.sourceConnection.database.schema,
						TableName: dataIntegration.sourceConnection.database.tableName,
						Query: dataIntegration.sourceConnection.database.query,
					}
					sourceConnections['Database'] = database
				}
				if (sourceColumns?.length > 0) {
					sourceConnections['Columns'] = sourceColumns.join()
				}
			}
			let targetConnections = null
			if (
				dataIntegration?.targetConnection &&
				dataIntegration?.targetConnection != null &&
				dataIntegration?.targetConnection?.connection?.name != null) {
				targetConnections = {
					ConnectionName: dataIntegration.targetConnection.connection.name,
				}

				if (dataIntegration?.targetConnection?.connection?.connectionTypeId === 1) {
					let database = {
						Schema: dataIntegration.targetConnection.database.schema,
						TableName: dataIntegration.targetConnection.database.tableName,
						Query: dataIntegration.targetConnection.database.query,
					}
					targetConnections['Database'] = database
				}
				if (targetColumns?.length > 0) {
					targetConnections['Columns'] = targetColumns.join()
				}
			}
			else {
				if (validate === true) {
					toast.error("Error on " + dataIntegration.code + ". Target Connection Required for integraion", { position: toast.POSITION.BOTTOM_RIGHT })
				}
				hasError = true
			}
			let integration = {
				Code: dataIntegration.code,
				IsTargetTruncate: dataIntegration.isTargetTruncate,
				IsDelta: false,
				Comments: dataIntegration.comments,
			}
			if (sourceConnections && sourceConnections != null) {
				integration['SourceConnections'] = sourceConnections
			}
			if (targetConnections && targetConnections != null) {
				integration['TargetConnections'] = targetConnections
			}
			if (integration && integration != null) {
				let operationIntegration = {
					Limit: dataOperationIntegration.limit,
					ProcessCount: dataOperationIntegration.processCount,
					Integration: integration,
				}
				if (operationIntegration && operationIntegration != null) {
					operationIntegrations = operationIntegrations.concat(operationIntegration)
				}
			}
		}
		if (hasError && validate === true) {
			return null
		}
		else {
			let operation = {
				Name: operationData.name,
				Contacts: contacts,
				Integrations: operationIntegrations
			}
			return operation
		}
	};


	const save = event => {
		let operationData = createOperationJson(values, true)
		if (operationData != null) {
			dispatch(postOperation(operationData));
		}
	};

	const clear = event => {
		initializeValues()
	};

	const deleteAction = () => {
		dispatch(deleteOperation({ id: parseInt(routeParams.id) }));

	}

	const applyDataOperationIntegrationsChange = (data, index) => {
		setValues({ ...values, integrations: data });
	}

	const applyDataOperationContactsChange = (data) => {
		setValues({ ...values, contacts: data });
	}

	const applyDataOperationChange = (data) => {
		setValues(data);
		setOpen(false)
	}

	const [open, setOpen] = React.useState(false);
	const [content, setContent] = React.useState('{}');
	const [oldJsonContent, setOldJsonContent] = React.useState('{}');
	const handleOpen = () => {

		let operationData = createOperationJson(values)
		let oldOperationJson = createOperationJson(operation)
		if (operationData != null) {
			setContent(JSON.stringify(operationData, null, "\t"))
			setOldJsonContent(oldOperationJson)
			setOpen(true);
		}
	};

	return (

		<React.Fragment>
			<Box>
				<form className={classes.root} noValidate autoComplete="off" style={{ padding: ' 0 0 15px 0' }}>
					<Grid container spacing={3}>
						<Grid item xs>
							<Box style={{ width: '100%' }}>
								<Grid container spacing={3}>
									<Grid item xs={3}>
										<TextField
											id="id"
											label="Id"
											type="number"
											fullWidth={true}
											InputLabelProps={{
												shrink: true,
											}}
											disabled={disabilityStatus.id}
											InputProps={{
												readOnly: readonlyStatus.id,
											}}
											value={checkValue(values.id)}
										/>
									</Grid>
									<Grid item xs>
										<TextField
											id="name"
											label="Name"
											fullWidth={true}
											InputLabelProps={{
												shrink: true,
											}}
											disabled={disabilityStatus.name}
											InputProps={{
												readOnly: readonlyStatus.name,
											}}
											value={values.name}
											onChange={handleChange('name')}
										/>
									</Grid>
								</Grid>
							</Box>
						</Grid>
						<Grid item xs>
							<Box style={{ width: '100%' }}>
								<Grid container spacing={3}>
									<Grid item xs={9}>
										<TextField
											id="definitionId"
											label="Definition Id"
											type="number"
											fullWidth={true}
											InputLabelProps={{
												shrink: true,
											}}
											disabled={disabilityStatus.definitionId}
											InputProps={{
												readOnly: readonlyStatus.definitionId,
											}}
											value={values.definitionId}
										/>
									</Grid>
									<Grid item xs={3}>
										<TextField
											id="version"
											label="Version"
											type="number"
											fullWidth={true}
											InputLabelProps={{
												shrink: true,
											}}
											disabled={disabilityStatus.version}
											InputProps={{
												readOnly: readonlyStatus.version,
											}}
											value={values.version}
										/>
									</Grid>
								</Grid>
							</Box>
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
											onChange={handleChange('creationDate')}
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
					</Grid>
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
										<Button
											variant="contained"
											color="primary"
											size="large"
											className={classes.button}
											startIcon={<Icon >upload_file</Icon>}
											onClick={handleOpen}
										>
											Definition
										</Button>
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
									</ButtonGroup>
								</Box>
							) : ("")
					}
				</form>

				<TabContext value={tabValue}>
					<AppBar position="static">

						{
							values.id && values.id !== null && values.id !== 0 ?
								(
									<TabList onChange={handleTabChange} aria-label="simple tabs example" >
										<Tab label="Details" value="1" />
										<Tab label="Jobs" value="3" />
										<Tab label="Executions" value="4" />
									</TabList>
								) : (
									<TabList onChange={handleTabChange} aria-label="simple tabs example" >
										<Tab label="Details" value="1" />
									</TabList>
								)
						}
					</AppBar>
					<TabPanel value="1">
						{
							values.contacts && values.contacts != null ? (
								<Box >
									<Typography variant="h4" gutterBottom component="div">
										Contacts
									</Typography>

									<DataOperationContactsData rowData={values.contacts} applyChange={applyDataOperationContactsChange} />
								</Box>
							) : ('')
						}
						{
							values.integrations && values.integrations != null ? (
								<Box >
									<Typography variant="h4" gutterBottom component="div">
										Integrations
									</Typography>
									<DataOperationIntegrationsData
										rowData={values.integrations}
										applyChange={applyDataOperationIntegrationsChange}
									/>
								</Box>
							) : ("")
						}
					</TabPanel>
					{
						values.id && values.id !== null && values.id !== 0 ? (
							<TabPanel value="3">
								<DataOperationJobs HasHeader={false} DataOperationId={values.id} />
							</TabPanel>
						) : ("")
					}
					{
						values.id && values.id !== null && values.id !== 0 ? (
							<TabPanel value="4">
								<DataOperationJobExecutions HasHeader={false} DataOperationId={values.id} />
							</TabPanel>
						) : ("")
					}
				</TabContext>
			</Box >

			<DataOperationJsonContent
				open={open} setOpen={setOpen}
				content={content} setContent={setContent}
				oldJsonContent={oldJsonContent}
				oldData={operation}
				applyChange={applyDataOperationChange}
			></DataOperationJsonContent>
		</React.Fragment>
	);
}

export default withRouter(DataOperationContent);
