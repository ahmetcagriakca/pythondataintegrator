import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getConnectionBigData, postConnectionBigData, checkBigDataConnection, clearBigDataConnection, checkBigDataTableRowCount, deleteBigDataConnection } from './store/connectionBigDataSlice';
import { getConnectionTypeName, selectConnectionTypeName } from './store/connectionTypeNameSlice';
import { getConnectorTypeName, selectConnectorTypeName } from './store/connectorTypeNameSlice';
import { getAuthenticationTypeName, selectAuthenticationTypeName } from './store/authenticationTypeNameSlice';
import Button from '@material-ui/core/Button';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Box from '@material-ui/core/Box';
import { DateTimePicker } from "@material-ui/pickers";

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

function ConnectionBigDataContent() {
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
		connectionType: { id: 4, name: 'BigData' },
		connectorType: null,
		host: '',
		port: null,
		databaseName: '',
		authenticationType: null,
		user: '',
		password: '',
		krbRealm: '',
		krbFqdn: '',
		krbServiceName: '',
		ssl: false,
		useOnlySspi: false,
		showPassword: false,
		creationDate: new Date(),
		isDeleted: true,
	});
	const [disabilityStatus, setDisabilityStatus] = React.useState({});
	const [readonlyStatus, setReadonlyStatus] = React.useState({});


	const selectConnectionTypeNames = useSelector(selectConnectionTypeName);
	const selectConnectorTypeNames = useSelector(selectConnectorTypeName);
	const selectAuthenticationTypeNames = useSelector(selectAuthenticationTypeName);


	const connection = useSelector(({ connectionBigDataApp }) => {
		return connectionBigDataApp.connectionBigData.data
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
			dispatch(getConnectionBigData(routeParams));
		}
		else {
			dispatch(clearBigDataConnection(routeParams));
		}
	}, [dispatch, routeParams]);

	useEffect(() => {
		if (connection && connection != null) {
			
			if (connection !== undefined) {
				let data= { ...connection }

				data.connectionType = { id: 4, name: 'BigData' }
				setValues(data);
			}
			else {
				let data = { ...values }
				data.connectionType = { id: 4, name: 'BigData' }
				setValues(data);
			}
			setDisabilityStatus({
				id: true,
				name: ((connection.id && connection.id !== null) || connection.isDeleted === 1) ? true : false,
				connectionType: true,
				// connectionType: ((connection.id && connection.id !== null) || connection.isDeleted === 1) ? true : false,
				connectorType: (connection.isDeleted === 1) ? true : false,
				host: (connection.isDeleted === 1),
				port: (connection.isDeleted === 1),
				databaseName: (connection.isDeleted === 1),
				authenticationType: (connection.isDeleted === 1),
				user: (connection.isDeleted === 1),
				password: (connection.isDeleted === 1),
				krbRealm: (connection.isDeleted === 1),
				krbFqdn: (connection.isDeleted === 1),
				krbServiceName: (connection.isDeleted === 1),
				ssl: (connection.isDeleted === 1),
				useOnlySspi: (connection.isDeleted === 1),
				showPassword: false,
				creationDate: true,
				isDeleted: true,
			})

			setReadonlyStatus({
				id: true,
				name: ((connection.id && connection.id !== null)) ? true : false,
				connectionType: true,
				// connectionType: ((connection.id && connection.id !== null)) ? true : false,
				connectorType: false,
				host: false,
				port: false,
				databaseName: false,
				authenticationType: false,
				user: false,
				password: false,
				krbRealm: false,
				krbFqdn: false,
				krbServiceName: false,
				ssl: false,
				useOnlySspi: false,
				showPassword: false,
				creationDate: true,
				isDeleted: true,
			})
		}
	}, [connection, selectConnectionTypeNames, selectConnectorTypeNames, selectAuthenticationTypeNames, setDisabilityStatus]);


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
		let record = { ...values }
		if (record.ssl === undefined) {
			record.ssl = false
		}
		if (record.useOnlySspi === undefined) {
			record.useOnlySspi = false
		}
		dispatch(postConnectionBigData(record));
	};

	const checkConnectionAction = event => {
		routeParams.ConnectionName = values.name
		dispatch(checkBigDataConnection(routeParams));
	};

	const deleteAction = event => {
		dispatch(deleteBigDataConnection({ id: parseInt(routeParams.id) }));
	};
	const handleClickShowPassword = () => {
		setValues({ ...values, showPassword: !values.showPassword });
	};

	const handleMouseDownPassword = (event) => {
		event.preventDefault();
	};

	const checkCountAction = event => {
		routeParams.ConnectionName = values.name
		routeParams.Schema = schema
		routeParams.Table = table
		dispatch(checkBigDataTableRowCount(routeParams));
	};
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
						<Autocomplete
							id="country-select-demo"
							style={{ width: '100%' }}
							fullWidth={true}
							autoHighlight
							clearOnEscape
							openOnFocus
							options={selectConnectorTypeNames.filter(data => data.connectionTypeId === values.connectionType?.id)}
							classes={{
								option: classes.option,
							}}
							filterOptions={filterOptions}
							getOptionLabel={(option) => option.name}
							renderOption={(option) => (
								<React.Fragment>
									<span>{option.name}</span>
								</React.Fragment>
							)}
							renderInput={(params) => (
								<TextField
									{...params}
									label="Connector type"
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
							value={values.connectorType}
							disabled={disabilityStatus.connectorType}
							readOnly={readonlyStatus.connectorType}
							onChange={(event, newValue) => {
								handleChangeValue(event, 'connectorType', newValue);
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
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField
							id="standard-name"
							label="Host"
							InputLabelProps={{
								shrink: true,
							}}
							disabled={disabilityStatus.host}
							readOnly={readonlyStatus.host}
							value={checkValue(values.host)}
							fullWidth={true} onChange={handleChange('host')} />
					</Grid>
					<Grid item xs={2}>
						<TextField
							id="standard-name"
							label="Port"
							type="number"
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							disabled={disabilityStatus.port}
							readOnly={readonlyStatus.port}
							value={checkValue(values.port)}
							onChange={handleChange('port')}
						/>
					</Grid>
				</Grid>
				<Grid container spacing={3}>

					<Grid item xs>
						<TextField
							id="standard-name"
							label="DatabaseName"
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							disabled={disabilityStatus.databaseName}
							readOnly={readonlyStatus.databaseName}
							value={checkValue(values.databaseName)}
							onChange={handleChange('databaseName')} />
					</Grid>
				</Grid>

				<Grid container spacing={3}>
					<Grid item xs>
						<Autocomplete
							id="country-select-demo"
							style={{ width: '100%' }}
							fullWidth={true}
							autoHighlight
							clearOnEscape
							openOnFocus
							options={selectAuthenticationTypeNames}
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
									label="Authentication type"
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
							disabled={disabilityStatus.authenticationType}
							readOnly={readonlyStatus.authenticationType}
							value={values.authenticationType}
							onChange={(event, newValue) => {
								handleChangeValue(event, 'authenticationType', newValue);
							}}
						/>
					</Grid>
				</Grid>
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField
							id="standard-name"
							label={values.authenticationType?.id == 1 ? "User" : "Principal"}
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							disabled={disabilityStatus.user}
							readOnly={readonlyStatus.user}
							value={checkValue(values.user)}
							onChange={handleChange('user')} />
					</Grid>
					<Grid item xs>

						<TextField
							id="outlined-basic"
							label='Password'
							fullWidth={true}
							type={values.showPassword ? 'text' : 'password'}
							InputProps={{
								endAdornment: (
									<InputAdornment position="end">
										<IconButton
											aria-label="toggle password visibility"
											edge="end"
											disabled={disabilityStatus.password}
											onClick={handleClickShowPassword}
											onMouseDown={handleMouseDownPassword}
										>
											{values.showPassword ? <Icon >visibility</Icon> : <Icon >visibility_off</Icon>}
										</IconButton>
									</InputAdornment>
								)
							}}
							InputLabelProps={{
								shrink: true,
							}}
							disabled={disabilityStatus.password}
							readOnly={readonlyStatus.password}
							value={checkValue(values.password)}
							onChange={handleChange('password')}
						/>
					</Grid>
				</Grid>
				<Grid container spacing={3}>
					{
						values.authenticationType?.id == 2 ? (
							<Grid item xs>
								<TextField
									id="standard-name"
									label="Kerberos Realm"
									fullWidth={true}
									InputLabelProps={{
										shrink: true,
									}}
									disabled={disabilityStatus.krbRealm}
									readOnly={readonlyStatus.krbRealm}
									value={checkValue(values.krbRealm)}
									onChange={handleChange('krbRealm')} />
							</Grid>
						) : ('')
					}
					{
						values.authenticationType?.id == 2 ? (
							<Grid item xs>
								<TextField
									id="standard-name"
									label="Kerberos Fqdn"
									fullWidth={true}
									InputLabelProps={{
										shrink: true,
									}}
									disabled={disabilityStatus.krbFqdn}
									readOnly={readonlyStatus.krbFqdn}
									value={checkValue(values.krbFqdn)}
									onChange={handleChange('krbFqdn')} />
							</Grid>
						) : ('')
					}
					{
						values.authenticationType?.id == 2 ? (
							<Grid item xs>
								<TextField
									id="standard-name"
									label="Kerberos Service Name"
									fullWidth={true}
									InputLabelProps={{
										shrink: true,
									}}
									disabled={disabilityStatus.krbServiceName}
									readOnly={readonlyStatus.krbServiceName}
									value={checkValue(values.krbServiceName)}
									onChange={handleChange('krbServiceName')} />
							</Grid>
						) : ('')
					}
				</Grid>
				<Grid container spacing={3}>
					<Grid item xs>

						<FormControlLabel
							id="standard-name"
							style={{ margin: "5px" }}
							control={
								<Checkbox
									name="ssl"
									checked={values?.ssl}
									onChange={(event, newValue) => {
										handleChangeValue(event, 'ssl', newValue);
									}} />
							}
							label="Ssl"
						/>
					</Grid>
					<Grid item xs>

						<FormControlLabel
							id="standard-name"
							style={{ margin: "5px" }}
							control={
								<Checkbox
									name="useOnlySspi"
									checked={values?.useOnlySspi}
									onChange={(event, newValue) => {
										handleChangeValue(event, 'useOnlySspi', newValue);
									}} />
							}
							label="Use Only Sspi"
						/>
					</Grid>
					<Grid item xs>
					</Grid>
					<Grid item xs>
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
											</ButtonGroup>
										) : ("")
									}
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
export default ConnectionBigDataContent;
