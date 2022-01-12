import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';
import Icon from '@material-ui/core/Icon';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Box from '@material-ui/core/Box';
import { DateTimePicker } from "@material-ui/pickers";
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import FormControl from '@material-ui/core/FormControl';

import { getConnection, clearConnection, deleteConnection,checkConnection,checkTableRowCount } from './store/connectionSlice';

import { postConnectionSql} from './store/connectionSqlSlice'
import { postConnectionBigData} from './store/connectionBigDataSlice'
import { getConnectionTypeName, selectConnectionTypeName } from './store/connectionTypeNameSlice';
import { getConnectorTypeName } from './store/connectorTypeNameSlice';
import { getAuthenticationTypeName } from './store/authenticationTypeNameSlice';

import ConnectionSqlContent from "./sql/ConnectionSqlContent"
import ConnectionBigDataContent from "./bigdata/ConnectionBigDataContent"

function ConnectionContent() {
	const dispatch = useDispatch();
	const classes = filterFormStyles();
	const filterOptions = createFilterOptions({
		matchFrom: 'any',
		stringify: option => {
			return option.name
		},
	});
	const checkValue = value => value ? value : ''

	const [values, setValues] = React.useState({
		id: null,
		name: '',
		connectionType: null,
		creationDate: new Date(),
		isDeleted: true,
		sql: null,
		bigData: null,
	});
	const [disabilityStatus, setDisabilityStatus] = React.useState({});
	const [readonlyStatus, setReadonlyStatus] = React.useState({});


	const selectConnectionTypeNames = useSelector(selectConnectionTypeName);


	const connection = useSelector(({ connectionApp }) => {
		return connectionApp.connection.data
	});

	const routeParams = useParams();

	useEffect(() => {
		if (values.connectorType && values.connectorType !== null && values.connectionType?.id !== values.connectorType?.connectionTypeId) {
			setValues({ ...values, connectorType: null });
		}
	}, [values.connectionType]);

	const handleChangeValue = (event, prop, value) => {
		setValues({ ...values, [prop]: value });
	};

	const handleChange = (prop) => (event) => {
		handleChangeValue(event, prop, event.target.type === 'number' ? (parseInt(event.target.value) || 0) : event.target.value)
	};

	useEffect(() => {
		dispatch(getConnectionTypeName(routeParams));
		dispatch(getConnectorTypeName(routeParams));
		dispatch(getAuthenticationTypeName(routeParams));
		if (routeParams.id && routeParams.id != null) {
			dispatch(getConnection(routeParams));
		}
		else {
			dispatch(clearConnection(routeParams));
		}
	}, [dispatch, routeParams]);

	useEffect(() => {
		if (connection && connection != null ) {
			setValues(connection);
			setDisabilityStatus({
				id: true,
				name: ((connection.id && connection.id !== null) || connection.isDeleted === 1) ? true : false,
				connectionType: ((connection.id && connection.id !== null) || connection.isDeleted === 1) ? true : false,
				creationDate: true,
				isDeleted: true,
			})

			setReadonlyStatus({
				id: true,
				name: ((connection.id && connection.id !== null)) ? true : false,
				connectionType: ((connection.id && connection.id !== null)) ? true : false,
				creationDate: true,
				isDeleted: true,
			})
		}
	}, [connection, selectConnectionTypeNames, setDisabilityStatus]);


	const [open, setOpen] = React.useState(false);
	const [schema, setSchema] = React.useState('');
	const [table, setTable] = React.useState('');

	const handleCheckCountOpen = () => {
		setOpen(true);
	};

	const handleCheckCountClose = () => {
		setOpen(false);
	};

	const save = event => {
		let record={}
		switch (values.connectionType.id) {
			case 1:
				record = { ...values.sql }
				record.name = values.name
				dispatch(postConnectionSql(record));
				break
			case 2:
				break
			case 3:
				break
			case 4:
				record = { ...values.bigData }
				record.name = values.name
				dispatch(postConnectionBigData(record));
				break
		}
	};

	const checkConnectionAction = event => {
		routeParams.ConnectionId = values.id
		dispatch(checkConnection(routeParams));
	};

	const deleteAction = event => {
		dispatch(deleteConnection({ id: parseInt(routeParams.id) }));
	};

	const checkCountAction = event => {
		routeParams.ConnectionId = values.id
		routeParams.Schema = schema
		routeParams.Table = table
		dispatch(checkTableRowCount(routeParams));
	};
	const applyConnectionSqlChange = (data, index) => {
		setValues({ ...values, sql: data });
	}
	const applyConnectionBigDataChange = (data, index) => {
		setValues({ ...values, bigData: data });
	}
	return (

		<React.Fragment>
			<form className={classes.root} noValidate autoComplete="off">
				<Grid container spacing={3}>

					<Grid item xs>
						<Box style={{ width: '100%' }}>
							<Grid container spacing={1}>
								<Grid item xs={3}>

									<TextField
										id="standard-name"
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
										onChange={handleChange('id')}
									/>
								</Grid>
								<Grid item xs>
									<TextField
										id="standard-name"
										label="Name"
										variant="outlined"
										fullWidth={true}
										InputLabelProps={{
											shrink: true,
										}}
										disabled={disabilityStatus.name}
										readOnly={readonlyStatus.name}
										value={checkValue(values.name)}
										onChange={handleChange('name')}
									/>
								</Grid>
							</Grid>
						</Box>
					</Grid>
					<Grid item xs>
						<Autocomplete
							id="country-select-demo"
							style={{ width: '100%' }}
							fullWidth={true}
							autoHighlight
							clearOnEscape
							openOnFocus
							options={selectConnectionTypeNames}
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
									label="Connection type"
									variant="outlined"
									inputProps={{
										...params.inputProps,
										autoComplete: 'new-password', // disable autocomplete and autofill
									}}
								/>
							)}
							InputLabelProps={{
								shrink: true,
							}}
							disabled={disabilityStatus.connectionType}
							readOnly={readonlyStatus.connectionType}
							value={values.connectionType}
							onChange={(event, newValue) => {
								handleChangeValue(event, 'connectionType', newValue);
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
										InputLabelProps={{
											shrink: true,
										}}
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
					values.connectionType?.id === 1 ? (
						<ConnectionSqlContent
							applyChange={applyConnectionSqlChange}
						></ConnectionSqlContent>
					) : ("")
				}
				{
					values.connectionType?.id === 4 ? (
						<ConnectionBigDataContent
							applyChange={applyConnectionBigDataChange}
						></ConnectionBigDataContent>
					) : ("")
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
										connection.id && connection.id != null ? (
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
										connection.id && connection.id != null ? (
											<ButtonGroup disableElevation variant="contained" color="primary"
												className={classes.button}>
												<Button
													variant="contained"
													color="secondary"
													size="large"
													startIcon={<Icon >check_circle_outline</Icon>}
													// startIcon={<SearchIcon />}
													onClick={checkConnectionAction}
												>
													Check Connection
												</Button>

												{
													connection.connectionType?.id && (connection.connectionType?.id == 1 || connection.connectionType?.id == 4) ? (
														<Button
															variant="contained"
															color="secondary"
															size="large"
															startIcon={<Icon >check_circle_outline</Icon>}
															// startIcon={<SearchIcon />}
															onClick={handleCheckCountOpen}
														>
															Check Count
														</Button>
													) : ("")
												}
											</ButtonGroup>
										) : ("")
									}
									{
										values.connectionType?.id && values.connectionType?.id !== null ? (
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
			<Dialog
				fullWidth={true}
				maxWidth={"sm"}
				open={open}
				onClose={handleCheckCountClose}
				aria-labelledby="max-width-dialog-title"
			>
				<DialogTitle id="max-width-dialog-title">Check Count</DialogTitle>
				<DialogContent>
					<Box style={{ width: '100%', padding: '10px 0 0 0' }}>

						<form className={classes.form} noValidate>
							<FormControl className={classes.formControl}>
								<Grid container>
									<Grid item xs={6}>
										<TextField
											label="Schema"
											variant="outlined"
											fullWidth={true}
											InputLabelProps={{
												shrink: true,
											}}
											value={schema}
											onChange={event => setSchema(event.target.value)}
										/>
									</Grid>
									<Grid item xs={6}
										style={{ padding: '0 0 0 5px' }}>
										<TextField
											label="Table"
											variant="outlined"
											fullWidth={true}
											InputLabelProps={{
												shrink: true,
											}}
											value={table}
											onChange={event => setTable(event.target.value)}
										/>
									</Grid>
								</Grid>
							</FormControl>
						</form>
					</Box>
				</DialogContent>
				<DialogActions>
					<Button
						onClick={checkCountAction}
						s variant="contained"
						color="secondary"
						size="large">
						Check
					</Button>
					<Button onClick={handleCheckCountClose} color="secondary">
						Close
					</Button>
				</DialogActions>
			</Dialog>
		</React.Fragment >
	);
}
export default ConnectionContent;
