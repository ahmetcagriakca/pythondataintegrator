import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

import { filterFormStyles } from '../../../common/styles/FilterFormStyles';
import { selectConnectionTypeName } from '../store/connectionTypeNameSlice';
import { selectConnectorTypeName } from '../store/connectorTypeNameSlice';
import { selectAuthenticationTypeName } from '../store/authenticationTypeNameSlice';
import { getConnectionBigData, clearBigDataConnection } from '../store/connectionBigDataSlice';

function ConnectionBigDataContent(props) {
	const { applyChange } = props;
	const dispatch = useDispatch();
	const routeParams = useParams();
	const classes = filterFormStyles();
	const filterOptions = createFilterOptions({
		matchFrom: 'any',
		stringify: option => {
			return option.name
		},
	});
	const changeApply = (newRows) => {
		if (newRows) {
			applyChange(newRows)
		} else {
			applyChange(values)
		}
	};
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

	const connection = useSelector(({ connectionApp }) => {
		return connectionApp.connection.data
	});
	const connectionBigData = useSelector(({ connectionApp }) => {
		return connectionApp.connectionBigData.data
	});


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
		if (connectionBigData && connectionBigData != null && Object.keys(connectionBigData).length > 0) {

			if (connectionBigData !== undefined) {
				let data = { ...connectionBigData }

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
				name: ((connectionBigData.id && connectionBigData.id !== null) || connectionBigData.isDeleted === 1) ? true : false,
				connectionType: true,
				// connectionType: ((connection.id && connection.id !== null) || connection.isDeleted === 1) ? true : false,
				connectorType: (connectionBigData.isDeleted === 1) ? true : false,
				host: (connectionBigData.isDeleted === 1),
				port: (connectionBigData.isDeleted === 1),
				databaseName: (connectionBigData.isDeleted === 1),
				authenticationType: (connectionBigData.isDeleted === 1),
				user: (connectionBigData.isDeleted === 1),
				password: (connectionBigData.isDeleted === 1),
				krbRealm: (connectionBigData.isDeleted === 1),
				krbFqdn: (connectionBigData.isDeleted === 1),
				krbServiceName: (connectionBigData.isDeleted === 1),
				ssl: (connectionBigData.isDeleted === 1),
				useOnlySspi: (connectionBigData.isDeleted === 1),
				showPassword: false,
				creationDate: true,
				isDeleted: true,
			})

			setReadonlyStatus({
				id: true,
				name: ((connectionBigData.id && connectionBigData.id !== null)) ? true : false,
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
	}, [connectionBigData, selectConnectionTypeNames, selectConnectorTypeNames, selectAuthenticationTypeNames, setDisabilityStatus]);


	const handleClickShowPassword = () => {
		setValues({ ...values, showPassword: !values.showPassword });
	};

	const handleMouseDownPassword = (event) => {
		event.preventDefault();
	};

	useEffect(() => {
		if (routeParams.id && routeParams.id != null && routeParams.id==connection.id && connection?.connectionType?.id == 4) {
			dispatch(getConnectionBigData(routeParams));
		}
		else {
			dispatch(clearBigDataConnection(routeParams));
		}
	}, [dispatch, connection, routeParams]);
	return (

		<React.Fragment>
			<form className={classes.root} noValidate autoComplete="off">
				<Grid container spacing={3}>
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
							fullWidth={true}
							onChange={handleChange('host')}
							onBlur={event => changeApply()}
						/>
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
							onBlur={event => changeApply()}
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
							onChange={handleChange('databaseName')}
							onBlur={event => changeApply()}
						/>
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
							onBlur={event => changeApply()}
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
							onChange={handleChange('user')}
							onBlur={event => changeApply()}
						/>
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
							onBlur={event => changeApply()}
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
									onChange={handleChange('krbRealm')}
									onBlur={event => changeApply()}
								/>
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
									onChange={handleChange('krbFqdn')}
									onBlur={event => changeApply()}
								/>
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
									onChange={handleChange('krbServiceName')}
									onBlur={event => changeApply()}
								/>
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
									}}
									onBlur={event => changeApply()}
								/>
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
									}}
									onBlur={event => changeApply()}
								/>
							}
							label="Use Only Sspi"
						/>
					</Grid>
					<Grid item xs>
					</Grid>
					<Grid item xs>
					</Grid>
				</Grid>

			</form>
		</React.Fragment >
	);
}
export default ConnectionBigDataContent;
