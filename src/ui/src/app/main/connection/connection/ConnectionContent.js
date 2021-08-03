import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getConnection, postConnection, checkConnection, clearConnection, deleteConnection } from './store/connectionSlice';
import { getConnectionTypeName, selectConnectionTypeName } from './store/connectionTypeNameSlice';
import { getConnectorTypeName, selectConnectorTypeName } from './store/connectorTypeNameSlice';
import Button from '@material-ui/core/Button';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Box from '@material-ui/core/Box';


function ConnectionContent() {
	const dispatch = useDispatch();
	const classes = filterFormStyles();
	const filterOptions = createFilterOptions({
		matchFrom: 'start',
		stringify: option => {
			return option.name
		},
	});

	const [values, setValues] = React.useState({
		id: null,
		name: '',
		connectionType: null,
		connectorType: null,
		host: '',
		port: null,
		sid: '',
		serviceName: '',
		databaseName: '',
		user: '',
		password: '',
		showPassword: false,
	});
	const [disabilityStatus, setDisabilityStatus] = React.useState({});

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

	const selectConnectionTypeNames = useSelector(selectConnectionTypeName);
	const selectConnectorTypeNames = useSelector(selectConnectorTypeName);

	const routeParams = useParams();

	const connection = useSelector(({ connectionApp }) => {
		return connectionApp.connection.data
	});

	useEffect(() => {
		dispatch(getConnectionTypeName(routeParams));
		dispatch(getConnectorTypeName(routeParams));
		if (routeParams.id && routeParams.id != null) {
			dispatch(getConnection(routeParams));
		}
		else {
			dispatch(clearConnection(routeParams));
		}
	}, [dispatch, routeParams]);

	useEffect(() => {
		if (connection && connection != null) {
			setValues(connection);
			setDisabilityStatus({
				id: true,
				name: ((connection.id && connection.id !== null) || connection.isDeleted === 1) ? true : false,
				connectionType: ((connection.id && connection.id !== null) || connection.isDeleted === 1) ? true : false,
				connectorType: (connection.isDeleted === 1) ? true : false,
				host: (connection.isDeleted === 1),
				port: (connection.isDeleted === 1),
				sid: (connection.isDeleted === 1),
				serviceName: (connection.isDeleted === 1),
				databaseName: (connection.isDeleted === 1),
				user: (connection.isDeleted === 1),
				password: (connection.isDeleted === 1),
				showPassword: false,
			})
		}
	}, [connection, selectConnectionTypeNames, selectConnectorTypeNames, setDisabilityStatus]);

	const save = event => {
		dispatch(postConnection(values));
	};

	const check = event => {
		routeParams.name = values.name
		dispatch(checkConnection(routeParams));
	};
	const deleteAction = event => {
		dispatch(deleteConnection({ id: parseInt(routeParams.id) }));
	};
	const handleClickShowPassword = () => {
		setValues({ ...values, showPassword: !values.showPassword });
	};

	const handleMouseDownPassword = (event) => {
		event.preventDefault();
	};

	const checkValue = value => value ? value : ''

	return (

			<form className={classes.root} noValidate autoComplete="off">
				<Grid container spacing={3}>
					<Grid item xs={1}>
						<TextField id="standard-name"
							disabled={disabilityStatus.id}
							label="Id"
							value={checkValue(values.id)}
							type="number"
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							onChange={handleChange('id')} />
					</Grid>
					<Grid item xs>
						<TextField id="standard-name"
							value={checkValue(values.name)}
							disabled={disabilityStatus.name}
							label="Name"
							fullWidth={true}
							InputLabelProps={{
								shrink: true,
							}}
							onChange={handleChange('name')} />
					</Grid>
					<Grid item xs>
						<Autocomplete
							id="country-select-demo"
							value={values.connectionType}
							disabled={disabilityStatus.connectionType}
							style={{ width: '100%' }}
							onChange={(event, newValue) => {
								handleChangeValue(event, 'connectionType', newValue);
							}}
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
							fullWidth={true}
							autoHighlight
							clearOnEscape
							openOnFocus
						/>
					</Grid>
					<Grid item xs>
						<Autocomplete
							id="country-select-demo"
							disabled={disabilityStatus.connectorType}
							style={{ width: '100%' }}
							value={values.connectorType}
							onChange={(event, newValue) => {
								handleChangeValue(event, 'connectorType', newValue);
							}}
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
							fullWidth={true}
							autoHighlight
							clearOnEscape
							openOnFocus
						/>
					</Grid>
				</Grid>
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="standard-name"
							disabled={disabilityStatus.host}
							label="Host"
							value={checkValue(values.host)}
							InputLabelProps={{
								shrink: true,
							}}
							fullWidth={true} onChange={handleChange('host')} />
					</Grid>
					<Grid item xs={2}>
						<TextField id="standard-name"
							disabled={disabilityStatus.port}
							label="Port"
							type="number"
							InputLabelProps={{
								shrink: true,
							}}
							value={checkValue(values.port)}
							fullWidth={true}
							onChange={handleChange('port')}
						/>
					</Grid>
				</Grid>
				{
					values.connectionType?.id === 1 ?
						(
							<Grid container spacing={3}>

								{
									values.connectorType?.id === 2 ?
										(
											<Grid item xs>
												<TextField id="standard-name"
													disabled={disabilityStatus.sid}
													label="Sid"
													value={checkValue(values.sid)}
													fullWidth={true} onChange={handleChange('sid')} />
											</Grid>
										) : ("")
								}
								{
									values.connectorType?.id === 2 ?
										(

											<Grid item xs>
												<TextField id="standard-name"
													disabled={disabilityStatus.serviceName}
													label="ServiceName"
													value={checkValue(values.serviceName)}
													fullWidth={true} onChange={handleChange('serviceName')} />
											</Grid>
										) : ("")
								}
								{
									values.connectorType?.id !== 2 ?
										(
											<Grid item xs>
												<TextField id="standard-name"
													disabled={disabilityStatus.databaseName}
													label="DatabaseName"
													value={checkValue(values.databaseName)}
													fullWidth={true} onChange={handleChange('databaseName')} />
											</Grid>
										) : ("")
								}
							</Grid>
						) : ("")
				}
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="standard-name"
							disabled={disabilityStatus.user}
							label="User"
							value={checkValue(values.user)}
							InputLabelProps={{
								shrink: true,
							}}
							fullWidth={true} onChange={handleChange('user')} />
					</Grid>
					<Grid item xs>

						<TextField
							InputProps={{
								endAdornment: (
									<InputAdornment position="end">
										<IconButton
											disabled={disabilityStatus.password}
											aria-label="toggle password visibility"
											onClick={handleClickShowPassword}
											onMouseDown={handleMouseDownPassword}
											edge="end"
										>
											{values.showPassword ? <Icon >visibility</Icon> : <Icon >visibility_off</Icon>}
										</IconButton>
									</InputAdornment>
								)
							}}
							id="outlined-basic"
							disabled={disabilityStatus.password}
							label={'Password'}
							InputLabelProps={{
								shrink: true,
							}}
							value={checkValue(values.password)}
							type={values.showPassword ? 'text' : 'password'}
							onChange={handleChange('password')}
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
											<Button
												variant="contained"
												color="secondary"
												size="large"
												className={classes.button}
												startIcon={<Icon >check_circle_outline</Icon>}
												// startIcon={<SearchIcon />}
												onClick={check}
											>
												Check Connection
											</Button>
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
	);
}
export default ConnectionContent;
