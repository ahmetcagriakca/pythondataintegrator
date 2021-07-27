import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';
import { getDataOperation, postOperation } from './store/dataOperationSlice';
import { getConnectionName, selectConnectionName } from './store/connectionNameSlice';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import Typography from '@material-ui/core/Typography';
import { DateTimePicker } from "@material-ui/pickers";
import Button from '@material-ui/core/Button';

import AppBar from '@material-ui/core/AppBar';
import Tab from '@material-ui/core/Tab';
import TabContext from '@material-ui/lab/TabContext';
import TabList from '@material-ui/lab/TabList';
import TabPanel from '@material-ui/lab/TabPanel';

import DataOperationJobExecutions from '../executions/DataOperationJobExecutions';
import DataOperationJobs from '../jobs/DataOperationJobs';

const useRowStyles = makeStyles({
	root: {
		'& > *': {
			borderBottom: 'unset',
		},
	},
});
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
	tableRowHeader: {
		height: 70
	},
	tableCell: {
		padding: '0px 16px',
		// backgroundColor: 'gainsboro',
		backgroundColor: '#006565',
		color: 'white',
		// '&:hover': {
		// 	backgroundColor: 'blue !important'
		// }
		hover: {
			'&:hover': {
				backgroundColor: 'green !important'
			}
		}
	},

	tableHeadCellAction: {
		width: '5px',
		padding: '0px 8px',
		// backgroundColor: 'gainsboro',
		backgroundColor: '#006565',
		color: 'white',
		// '&:hover': {
		// 	backgroundColor: 'blue !important'
		// }
		hover: {
			'&:hover': {
				backgroundColor: 'green !important'
			}
		}
	},
	tableBodyCellAction: {
		width: '5px',
		padding: '0px 8px',
		color: 'white',
		hover: {
			'&:hover': {
				backgroundColor: 'green !important'
			}
		}
	}
}));

const StyledTableCell = withStyles((theme) => ({
	head: {
		color: theme.palette.common.white,
	},
	body: {
		fontSize: 14,
	},
}))(TableCell);
const StyledTableRow = withStyles((theme) => ({
	root: {
		'&:nth-of-type(2n+1)': {
			backgroundColor: theme.palette.action.hover,
		},
	},
}))(TableRow);

const StyledTableRow4n = withStyles((theme) => ({
	root: {
		'&:nth-of-type(4n+1)': {
			backgroundColor: theme.palette.action.hover,
		},
	},
}))(TableRow);
// function DataOperationIntegrationRow() {

function DataOperationContent() {
	const rowClasses = useRowStyles();
	const classes = useStyles();
	const dispatch = useDispatch();
	const formClasses = filterFormStyles();

	const [values, setValues] = React.useState({
		name: '',
		definitionId: 0,
		creationDate: new Date(),
		isDeleted: 0,
		contacts: [],
		integrations: [],
	});

	const handleChange = (prop) => (event) => {
		setValues({ ...values, [prop]: event.target.value });
	};

	const selectConnectionNames = useSelector(selectConnectionName);

	const routeParams = useParams();

	const operation = useSelector(({ dataOperationApp }) => {
		return dataOperationApp.dataOperation.entities[routeParams.id]
	});

	useEffect(() => {
		dispatch(getConnectionName(routeParams));
		dispatch(getDataOperation(routeParams));
	}, [dispatch, routeParams]);

	useEffect(() => {
		if (operation && operation != null) {
			let operationData = { ...operation }

			let integrationDatas = [...operationData.integrations]
			for (var i = 0; i < integrationDatas.length; i++) {
				let integration = { ...integrationDatas[i] }
				integration['open'] = false
				integrationDatas[i] = integration
			}
			operationData.integrations = integrationDatas
			setValues(operationData);
		}
	}, [operation, selectConnectionNames]);

	const uuid = () => {
		return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
			var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
			return v.toString(16);
		});
	}
	const checkValue = value => value ? value : ''

	const handleContactChange = (event, contact, index, prop) => {
		let newSetData = [...values.contacts];
		let newSet = { ...newSetData[index] };
		newSet[prop] = event.target.value
		newSetData[index] = newSet
		setValues({ ...values, contacts: newSetData });
	};
	const deleteContact = (event, contact, index) => {
		let newSet = [...values.contacts];
		newSet.splice(index, 1)
		setValues({ ...values, contacts: newSet });
	}
	const addContact = (event) => {
		let newSet = [...values.contacts];

		newSet = newSet.concat({ id: uuid(), email: "" })
		setValues({ ...values, contacts: newSet });
	}

	const handleIntegrationChange = (event, contact, index, prop) => {
		let newSetData = [...values.integrations];
		let newSet = { ...newSetData[index] };
		let propsplits = prop.split('.')

		if (propsplits.length === 0) {
		}
		else if (propsplits.length === 1) {
			newSet[propsplits[0]] = event.target.value
		}
		else if (propsplits.length === 2) {

			let newSubSet = { ...newSet[propsplits[0]] };
			newSubSet[propsplits[1]] = event.target.value
			newSet[propsplits[0]] = newSubSet
		}
		else if (propsplits.length === 3) {
			let newSubSet1 = { ...newSet[propsplits[0]] };
			let newSubSet2 = { ...newSubSet1[propsplits[1]] };
			newSubSet2[propsplits[2]] = event.target.value
			newSubSet1[propsplits[1]] = newSubSet2
			newSet[propsplits[0]] = newSubSet1
		}
		else if (propsplits.length === 4) {

			let newSubSet1 = { ...newSet[propsplits[0]] };
			let newSubSet2 = { ...newSubSet1[propsplits[1]] };
			let newSubSet3 = { ...newSubSet2[propsplits[2]] };
			newSubSet3[propsplits[3]] = event.target.value
			newSubSet2[propsplits[2]] = newSubSet3
			newSubSet1[propsplits[1]] = newSubSet2
			newSet[propsplits[0]] = newSubSet1
		}
		newSetData[index] = newSet
		setValues({ ...values, integrations: newSetData });
	};
	const deleteIntegration = (event, contact, index) => {
		let newSet = [...values.integrations];
		newSet.splice(index, 1)
		setValues({ ...values, integrations: newSet });
	}
	const addIntegration = (event) => {
		let newSet = [...values.integrations];

		newSet = newSet.concat(
			{
				id: uuid(),
				limit: 0,
				processCount: 0,
				integration: {
					id: uuid(),
					code: '',
					isTargetTruncate: false,
					comments: '',
					sourceConnection: {
						id: uuid(),
						connection: {
							id: uuid(),
							database: {
								id: uuid(),
								connectorType: {
									id: uuid(),
								}
							},
							connectionType: {
								id: uuid(),
							}
						},
						database: {
							id: uuid(),
						}
					},
					targetConnection: {
						id: uuid(),
						connection: {
							id: uuid(),
							database: {
								id: uuid(),
								connectorType: {
									id: uuid(),
								}
							},
							connectionType: {
								id: uuid(),
							}
						},
						database: {
							id: uuid(),
						}
					},
					columns: [
					]
				}
			}
		)
		setValues({ ...values, integrations: newSet });
	}

	const handleColumnChange = (event, row, integrationIndex, index, prop) => {

		let newSetOperationIntegrations = [...values.integrations];
		let newSetOperationIntegration = { ...newSetOperationIntegrations[integrationIndex] };
		let newSetIntegration = { ...newSetOperationIntegration.integration };
		let newSetColumns = [...newSetIntegration.columns];
		let newSetColumn = { ...newSetColumns[index] };
		newSetColumn[prop] = event.target.value
		newSetColumns[index] = newSetColumn
		newSetIntegration.columns = newSetColumns
		newSetOperationIntegration.integration = newSetIntegration
		newSetOperationIntegrations[integrationIndex] = newSetOperationIntegration
		setValues({ ...values, integrations: newSetOperationIntegrations });
	};
	const deleteColumn = (event, row, integrationIndex, index) => {
		let newSetOperationIntegrations = [...values.integrations];
		let newSetOperationIntegration = { ...newSetOperationIntegrations[integrationIndex] };
		let newSetIntegration = { ...newSetOperationIntegration.integration };
		let newSetColumns = [...newSetIntegration.columns];
		newSetColumns.splice(index, 1)
		newSetIntegration.columns = newSetColumns
		newSetOperationIntegration.integration = newSetIntegration
		newSetOperationIntegrations[integrationIndex] = newSetOperationIntegration
		setValues({ ...values, integrations: newSetOperationIntegrations });
	}
	const addColumn = (event, integrationIndex) => {
		let newSetOperationIntegrations = [...values.integrations];
		let newSetOperationIntegration = { ...newSetOperationIntegrations[integrationIndex] };
		let newSetIntegration = { ...newSetOperationIntegration.integration };
		let newSetColumns = [...newSetIntegration.columns];
		newSetColumns = newSetColumns.concat({ id: uuid() })
		newSetIntegration.columns = newSetColumns
		newSetOperationIntegration.integration = newSetIntegration
		newSetOperationIntegrations[integrationIndex] = newSetOperationIntegration
		setValues({ ...values, integrations: newSetOperationIntegrations });
	}

	const changeOpen = (row, index) => {
		let newSetOperationIntegrations = [...values.integrations];
		let newSetOperationIntegration = { ...newSetOperationIntegrations[index] };
		newSetOperationIntegration.open = !row.open
		newSetOperationIntegrations[index] = newSetOperationIntegration
		setValues({ ...values, integrations: newSetOperationIntegrations });
	}
	const save = event => {
		let contacts = []
		for (var i = 0; i < values.contacts.length; i++) {
			contacts = contacts.concat({ Email: values.contacts[i].email })
		}

		let integrations = []
		for (var j = 0; j < values.integrations.length; j++) {
			let sourceColumns = []
			let targetColumns = []
			for (var k = 0; k < values.integrations[j].integration.columns.length; k++) {
				sourceColumns = sourceColumns.concat(values.integrations[j].integration.columns[k].sourceColumnName)
				targetColumns = targetColumns.concat(values.integrations[j].integration.columns[k].targetColumnName)
			}
			integrations = integrations.concat({
				Limit: values.integrations[j].limit,
				ProcessCount: values.integrations[j].processCount,
				Integration: {
					Code: values.integrations[j].integration.code,
					IsTargetTruncate: values.integrations[j].integration.isTargetTruncate,
					IsDelta: false,
					Comments: (values.integrations[j].integration.comments && values.integrations[j].integration.comments !== null) ? values.integrations[j].integration.comments : '',
					SourceConnections: {
						ConnectionName: values.integrations[j].integration.sourceConnection.connection.name,
						Database: {
							Schema: values.integrations[j].integration.sourceConnection.database.schema,
							TableName: values.integrations[j].integration.sourceConnection.database.tableName,
							Query: values.integrations[j].integration.sourceConnection.database.query,
						},
						Columns: sourceColumns.join()
					},
					TargetConnections: {
						ConnectionName: values.integrations[j].integration.targetConnection.connection.name,
						Database: {
							Schema: values.integrations[j].integration.targetConnection.database.schema,
							TableName: values.integrations[j].integration.targetConnection.database.tableName,
							Query: values.integrations[j].integration.targetConnection.database.query,
						},
						Columns: targetColumns.join()
					}
				}
			})
		}
		let operation = {
			Name: values.name,
			Contacts: contacts,
			Integrations: integrations
		}
		dispatch(postOperation(operation));
	};

	const clear = event => {
		if (operation && operation != null) {
			setValues(operation);
		}
	};

	const [tabValue, setTabValue] = React.useState('1');
	const handleTabChange = (event, newValue) => {

		setTabValue(newValue);
	};
	return (

		<div className={formClasses.root}
			style={{ padding: '15px 40px 15px 40px' }}
		>
			<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>

			<form className={classes.root} noValidate autoComplete="off" style={{ padding: ' 0 0 15px 0' }}>
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="name" label="Name" value={values.name}
							disabled

							fullWidth={true} onChange={handleChange('name')} />
					</Grid>
					<Grid item xs>
						<TextField id="definitionId" label="Definition Id" value={values.definitionId}
							disabled
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}} onChange={handleChange('definitionId')} />
					</Grid>
					<Grid item xs>
						<DateTimePicker
							disabled
							fullWidth={true}
							label="Creation Date"
							inputVariant="outlined"
							value={values.creationDate}
							onChange={handleChange('creationDate')}
							format="DD/MM/yyyy HH:mm:sss a"
						/>
					</Grid>
					<Grid item xs>
						<TextField id="isDeleted" label="Is Deleted" value={values.isDeleted}
							disabled
							fullWidth={true}
							type="number"
							InputLabelProps={{
								shrink: true,
							}} onChange={handleChange('name')} />
					</Grid>
				</Grid>

				<Grid container spacing={3}>
					<Grid item xs>
					</Grid>
					<Grid item xs={1}>
						<Button
							variant="contained"
							color="secondary"
							size="large"
							onClick={clear}
						>
							Clear
						</Button>
					</Grid>
					<Grid item xs={1}>
						<Button
							variant="contained"
							color="secondary"
							size="large"
							onClick={save}
						>
							Save
						</Button>
					</Grid>
				</Grid>
			</form>

			<TabContext value={tabValue}>
				<AppBar position="static">
					<TabList onChange={handleTabChange} aria-label="simple tabs example" >
						<Tab label="Definition" value="1" />
						{/* <Tab label="Definitions" value="2" />*/}
						<Tab label="Jobs" value="3" />
						<Tab label="Executions" value="4" />
					</TabList>
				</AppBar>
				<TabPanel value="1">
					<Box >
						{
							values.contacts && values.contacts !== null ? (
								<Table size="small" >
									<caption>

										<IconButton aria-label="expand row" key={'cellContactAddAction'} size="small" onClick={event => addContact(event)}>
											<Icon className="text-16 arrow-icon" style={{ color: 'green' }}>
												add_circle
											</Icon>
										</IconButton>
									</caption>
									<TableHead>
										<TableRow key={'headRowContact'} className={classes.tableRowHeader}>
											<StyledTableCell key={'headCellContactEmail'} align={'left'} padding={'normal'} className={classes.tableCell}> Email </StyledTableCell>
											<StyledTableCell key={'headCellContactAction'} align={'left'} padding={'normal'} className={classes.tableHeadCellAction}> Action </StyledTableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{values.contacts.map((contactRow, i) => (
											<StyledTableRow key={'bodyRowContact' + contactRow.id}>
												<StyledTableCell key={'bodyCellContactEmail' + contactRow.id} >

													<TextField id="name" label="" value={contactRow.email} InputLabelProps={{ shrink: false }} fullWidth={true}
														onChange={event => handleContactChange(event, contactRow, i, 'email')} />
												</StyledTableCell>
												<StyledTableCell key={'bodyCellContactDeleteAction' + contactRow.id} className={classes.tableBodyCellAction}>

													<IconButton aria-label="expand row" key={'cellContactDeleteAction' + contactRow.id} size="small"
														onClick={event => deleteContact(event, contactRow, i)}>
														<Icon className="text-16 arrow-icon" style={{ color: 'red' }}>
															remove_circle
														</Icon>
													</IconButton>
												</StyledTableCell>
											</StyledTableRow>
										))}
									</TableBody>
								</Table>
							) :
								("")
						}
					</Box>

					<Box >
						<Typography variant="h4" gutterBottom component="div">
							Integrations
						</Typography>
						{
							values.integrations && values.integrations !== null ? (
								<Table size="small" >
									<caption>

										<IconButton aria-label="expand row" key={'cellIntegrationAddAction'} size="small" onClick={event => addIntegration(event)}>
											<Icon className="text-16 arrow-icon" style={{ color: 'green' }}>
												add_circle
											</Icon>
										</IconButton>
									</caption>
									<TableHead>
										<TableRow key={'headRowIntegration'} className={classes.tableRowHeader}>
											<StyledTableCell key={'headRowIntegrationCollapse'} align={'left'} padding={'normal'} className={classes.tableCell}>  </StyledTableCell>
											<StyledTableCell key={'headRowIntegrationCode'} align={'left'} padding={'normal'} className={classes.tableCell}> Code </StyledTableCell>
											<StyledTableCell key={'headRowIntegrationLimit'} align={'left'} padding={'normal'} className={classes.tableCell}> Limit </StyledTableCell>
											<StyledTableCell key={'headRowIntegrationProcessCount'} align={'left'} padding={'normal'} className={classes.tableCell}> Process Count </StyledTableCell>
											<StyledTableCell key={'headRowIntegrationSourceConnectionName'} align={'left'} padding={'normal'} className={classes.tableCell}> Source Connection  </StyledTableCell>
											<StyledTableCell key={'headRowIntegrationTargetConnectionName'} align={'left'} padding={'normal'} className={classes.tableCell}> Target Connection  </StyledTableCell>
											<StyledTableCell key={'headRowIntegrationIsTargetTruncate'} align={'left'} padding={'normal'} className={classes.tableCell}> Is Target Truncate </StyledTableCell>
											<StyledTableCell key={'headRowIntegrationComments'} align={'left'} padding={'normal'} className={classes.tableCell}> Comments </StyledTableCell>
											<StyledTableCell key={'headRowIntegrationAction'} align={'left'} padding={'normal'} className={classes.tableCell}> Action </StyledTableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{values.integrations.map((integrationRow, integrationIndex) => (
											<React.Fragment>
												<StyledTableRow4n key={'bodyRowIntegration' + integrationRow.id} className={rowClasses.root}>
													<StyledTableCell key={'bodyCellIntegrationCollapse' + integrationRow.id} >
														<IconButton aria-label="expand row" size="small" onClick={() => changeOpen(integrationRow, integrationIndex)}>
															<Icon className="text-16 arrow-icon" color="inherit">
																{integrationRow.open ? 'expand_less' : 'expand_more'}
															</Icon>
														</IconButton>
													</StyledTableCell>
													<StyledTableCell key={'bodyCellIntegrationCode' + integrationRow.id} component="th" scope="row">{integrationRow.integration.code}</StyledTableCell>
													<StyledTableCell key={'bodyCellIntegrationLimit' + integrationRow.id} align="left">{integrationRow.limit}</StyledTableCell>
													<StyledTableCell key={'bodyCellIntegrationProcessCount' + integrationRow.id} align="left">{integrationRow.processCount}</StyledTableCell>
													<StyledTableCell key={'bodyCellIntegrationSourceConnectionName' + integrationRow.id} align="left">{checkValue(integrationRow.integration.sourceConnection.connection.name) + '-' + checkValue(integrationRow.integration.sourceConnection.connection.database.connectorType.name)}</StyledTableCell>
													<StyledTableCell key={'bodyCellIntegrationTargetConnectionName' + integrationRow.id} align="left">{checkValue(integrationRow.integration.targetConnection.connection.name) + '-' + checkValue(integrationRow.integration.targetConnection.connection.database.connectorType.name)}</StyledTableCell>
													<StyledTableCell key={'bodyCellIntegrationIsTargetTruncate' + integrationRow.id} align="left">{integrationRow.integration.isTargetTruncate ? 'true' : 'false'}</StyledTableCell>
													<StyledTableCell key={'bodyCellIntegrationComments' + integrationRow.id} align="left">{integrationRow.integration.comments}</StyledTableCell>

													<StyledTableCell key={'bodyCellIntegrationDeleteAction' + integrationRow.id}>
														<IconButton aria-label="expand row" key={'cellIntegrationDeleteAction' + integrationRow.id} size="small" onClick={event => deleteIntegration(event, integrationRow, integrationIndex)}>
															<Icon className="text-16 arrow-icon" style={{ color: 'red' }}>
																remove_circle
															</Icon>
														</IconButton>
													</StyledTableCell>
												</StyledTableRow4n>
												<TableRow key={'bodyRowIntegrationBox' + integrationRow.id}>
													<TableCell key={'bodyCellIntegrationBox' + integrationRow.id} style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={12}>
														<Collapse key={'integrationBoxCollapse' + integrationRow.id} in={integrationRow.open} timeout="auto" unmountOnExit>
															<Box key={'integrationBox' + integrationRow.id}>
																<Typography key={'integrationBoxTypography' + integrationRow.id} variant="h6" gutterBottom component="div">
																	Integration
																</Typography>
																<Grid container spacing={3}>
																	<Grid item xs>
																		<TextField id="standard-name" label="Limit" value={checkValue(integrationRow.limit)}
																			fullWidth={true} onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'limit')} />
																	</Grid>
																	<Grid item xs>
																		<TextField id="standard-name" label="Process Count" value={checkValue(integrationRow.processCount)}
																			fullWidth={true} onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'processCount')} />
																	</Grid>
																	<Grid item xs>
																	</Grid>
																	<Grid item xs>
																	</Grid>
																</Grid>
																<Grid container spacing={3}>
																	<Grid item xs>
																		<TextField id="standard-name" label="Code" value={checkValue(integrationRow.integration.code)}
																			fullWidth={true} onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.code')} />
																	</Grid>
																	<Grid item xs>
																		<TextField id="standard-name" label="Is Target Truncate" value={checkValue(integrationRow.integration.isTargetTruncate)}
																			fullWidth={true} onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.isTargetTruncate')} />
																	</Grid>
																	<Grid item xs>
																		<TextField id="standard-name" label="Comments" value={checkValue(integrationRow.integration.comments)}
																			fullWidth={true} onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.comments')} />
																	</Grid>
																	<Grid item xs>
																	</Grid>
																</Grid>
																<Divider className={classes.divider} />
																<Grid container spacing={3}>

																	<Grid item xs={6} >
																		<Box margin={1}>
																			<Typography variant="h6" gutterBottom component="div">
																				Source Connection
																			</Typography>

																			<Grid container spacing={1}>
																				<Grid item xs={6}>
																					<TextField id="standard-name" label="ConnectionName" value={checkValue(integrationRow.integration.sourceConnection.connection.name)}
																						fullWidth={true}
																						onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.sourceConnection.connection.name')} />
																				</Grid>
																				<Grid item xs={6}>
																				</Grid>
																				<Grid item xs={6}>
																					<TextField id="standard-name" label="Schema" value={checkValue(integrationRow.integration.sourceConnection.database.schema)}
																						fullWidth={true}
																						onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.sourceConnection.database.schema')} />
																				</Grid>
																				<Grid item xs={6}>
																					<TextField id="standard-name" label="Table" value={checkValue(integrationRow.integration.sourceConnection.database.tableName)}
																						fullWidth={true}
																						onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.sourceConnection.database.tableName')} />
																				</Grid>
																				<Grid item xs={12}>

																					<TextField
																						id="outlined-textarea"
																						label="Query" value={checkValue(integrationRow.integration.sourceConnection.database.query)}
																						placeholder="Source Connection Query"
																						multiline
																						minrows={4}
																						maxrows={4}
																						fullWidth={true}
																						variant="outlined"
																						inputProps={{ className: classes.textarea }}
																						onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.sourceConnection.database.query')}
																					/>
																				</Grid>
																			</Grid>
																		</Box>
																	</Grid>
																	<Grid item style={{ margin: "0 0 0 5" }} xs={6} >
																		<Box margin={1}>
																			<Typography variant="h6" gutterBottom component="div">
																				Target Connection
																			</Typography>
																			<Grid container spacing={1}>

																				<Grid item xs={6}>
																					<TextField id="standard-name" label="ConnectionName" value={checkValue(integrationRow.integration.targetConnection.connection.name)}
																						fullWidth={true}
																						onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.targetConnection.connection.name')} />
																				</Grid>
																				<Grid item xs={6}>
																				</Grid>
																				<Grid item xs={6}>
																					<TextField id="standard-name" label="Schema" value={checkValue(integrationRow.integration.targetConnection.database.schema)}
																						fullWidth={true}
																						onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.targetConnection.database.schema')} />
																				</Grid>
																				<Grid item xs={6}>
																					<TextField id="standard-name" label="Table" value={checkValue(integrationRow.integration.targetConnection.database.tableName)}
																						fullWidth={true}
																						onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.targetConnection.database.tableName')} />
																				</Grid>
																				<Grid item xs={12}>

																					<TextField
																						id="outlined-textarea"
																						label="Query" value={checkValue(integrationRow.integration.targetConnection.database.query)}
																						placeholder="Target Connection Query"
																						multiline
																						minrows={4}
																						maxrows={4}
																						fullWidth={true}
																						variant="outlined"
																						inputProps={{ className: classes.textarea }}
																						onChange={event => handleIntegrationChange(event, integrationRow, integrationIndex, 'integration.targetConnection.database.query')}
																					/>
																				</Grid>
																			</Grid>
																		</Box>
																	</Grid>
																</Grid>
																<Grid container spacing={3}>

																	<Grid item xs={6} >
																		<Box margin={1}>
																			<Typography variant="h6" gutterBottom component="div">
																				Source Columns
																			</Typography>
																			<Grid item xs={12}>

																				{
																					integrationRow.integration.columns && integrationRow.integration.columns !== null ? (

																						<Table size="small" >
																							<caption>

																								<IconButton aria-label="expand row" key={'cellColumnAddAction'} size="small"
																									onClick={event => addColumn(event, integrationIndex)}>
																									<Icon className="text-16 arrow-icon" style={{ color: 'green' }}>
																										add_circle
																									</Icon>
																								</IconButton>
																							</caption>
																							<TableHead>
																								<TableRow key={'headRowIntegrationSourceColumns'} className={classes.tableRowHeader}>
																									<TableCell key={'headCellIntegrationColumnAction'} align={'left'} padding={'normal'} className={classes.tableHeadCellAction}>  </TableCell>
																									<TableCell key={'headCellIntegrationSourceColumnsColumn'} align={'left'} padding={'normal'} className={classes.tableCell}> Name </TableCell>
																								</TableRow>
																							</TableHead>
																							<TableBody>
																								{integrationRow.integration.columns.map((columnRow, columnIndex) => (

																									<StyledTableRow key={'bodyRowIntegrationSourceColumn' + columnRow.id}>
																										<StyledTableCell key={'bodyCellColumnDeleteAction' + columnRow.id} className={classes.tableBodyCellAction}>

																											<IconButton key={'cellColumnDeleteAction' + columnRow.id}
																												size="small" aria-label="expand row"
																												onClick={event => deleteColumn(event, columnRow, integrationIndex, columnIndex)}>
																												<Icon className="text-16 arrow-icon" style={{ color: 'red' }}>
																													remove_circle
																												</Icon>
																											</IconButton>
																										</StyledTableCell>
																										<StyledTableCell key={'bodyCellIntegrationSourceColumnName' + columnRow.id} >

																											<TextField key={'bodyCellTextIntegrationSourceColumnName' + columnRow.id}
																												id="name" label="" value={columnRow.sourceColumnName}
																												InputLabelProps={{ shrink: false }} fullWidth={true}
																												onChange={event => handleColumnChange(event, columnRow, integrationIndex, columnIndex, 'sourceColumnName')} />
																										</StyledTableCell>
																									</StyledTableRow>
																								))}
																							</TableBody>

																						</Table>
																					) :
																						("")
																				}
																			</Grid>
																		</Box>
																	</Grid>
																	<Grid item xs={6} >
																		<Box margin={1}>
																			<Typography variant="h6" gutterBottom component="div">
																				Target Columns
																			</Typography>
																			<Grid item xs={12}>
																				{
																					integrationRow.integration.columns && integrationRow.integration.columns !== null ? (

																						<Table size="small" >
																							<TableHead>
																								<TableRow key={'headRowIntegrationTargetColumns'} className={classes.tableRowHeader}>
																									<TableCell key={'headCellIntegrationTargetColumnsColumn'} align={'left'} padding={'normal'} className={classes.tableCell}> Name </TableCell>
																								</TableRow>
																							</TableHead>
																							<TableBody>

																								{integrationRow.integration.columns.map((columnRow, columnIndex) => (
																									<StyledTableRow key={'bodyRowIntegrationTargetColumn' + columnRow.id}>
																										<StyledTableCell key={'bodyCellIntegrationTargetColumnName' + columnRow.id} >
																											<TextField key={'bodyCellTextIntegrationTargetColumnName' + columnRow.id}
																												id="name" label="" value={columnRow.targetColumnName}
																												InputLabelProps={{ shrink: false }} fullWidth={true}
																												onChange={event => handleColumnChange(event, columnRow, integrationIndex, columnIndex, 'targetColumnName')} />
																										</StyledTableCell>
																									</StyledTableRow>
																								))}
																							</TableBody>
																						</Table>
																					) :
																						("")
																				}
																			</Grid>
																		</Box>
																	</Grid>
																</Grid>


																<Divider className={classes.divider} />
															</Box>
														</Collapse>
													</TableCell>
												</TableRow>
											</React.Fragment>
										))}
									</TableBody>
								</Table>
							) :
								("")
						}
					</Box>

				</TabPanel>
				<TabPanel value="3">
					{
						values.id && values.id !== null && values.id !== 0 ? (
							<DataOperationJobs HasHeader={false} DataOperationId={values.id} />
						) :
							("")
					}
				</TabPanel>
				<TabPanel value="4">
					{
						values.id && values.id !== null && values.id !== 0 ? (
							<DataOperationJobExecutions HasHeader={false} DataOperationId={values.id} />
						) :
							("")
					}
				</TabPanel>
			</TabContext>
		</div>
	);
}

export default withRouter(DataOperationContent);
