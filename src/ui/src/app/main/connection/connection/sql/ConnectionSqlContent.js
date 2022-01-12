import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';

import { selectConnectionTypeName } from '../store/connectionTypeNameSlice';
import { selectConnectorTypeName } from '../store/connectorTypeNameSlice';
import { filterFormStyles } from '../../../common/styles/FilterFormStyles';
import { getConnectionSql, clearSqlConnection } from '../store/connectionSqlSlice';

function ConnectionSqlContent(props) {
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
		connectionType: { id: 1, name: 'SQL' },
		connectorType: null,
		host: '',
		port: null,
		sid: '',
		serviceName: '',
		databaseName: '',
		user: '',
		password: '',
		showPassword: false,
		creationDate: new Date(),
		isDeleted: true,
	});

	const [disabilityStatus, setDisabilityStatus] = React.useState({});
	const [readonlyStatus, setReadonlyStatus] = React.useState({});

	const selectConnectionTypeNames = useSelector(selectConnectionTypeName);
	const selectConnectorTypeNames = useSelector(selectConnectorTypeName);

	const connection = useSelector(({ connectionApp }) => {
		return connectionApp.connection.data
	});
	const connectionSql = useSelector(({ connectionApp }) => {
		return connectionApp.connectionSql.data
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
		if (connectionSql && connectionSql != null && Object.keys(connectionSql).length > 0) {
			if (connectionSql !== undefined) {
				let data = { ...connectionSql }

				data.connectionType = { id: 1, name: 'SQL' }
				setValues(data);
			}
			else {
				let data = { ...values }
				data.connectionType = { id: 1, name: 'SQL' }
				setValues(data);
			}
			setDisabilityStatus({
				id: true,
				name: ((connectionSql.id && connectionSql.id !== null) || connectionSql.isDeleted === 1) ? true : false,
				connectionType: true,
				// connectionType: ((connectionSql.id && connectionSql.id !== null) || connectionSql.isDeleted === 1) ? true : false,
				connectorType: (connectionSql.isDeleted === 1) ? true : false,
				host: (connectionSql.isDeleted === 1),
				port: (connectionSql.isDeleted === 1),
				sid: (connectionSql.isDeleted === 1),
				serviceName: (connectionSql.isDeleted === 1),
				databaseName: (connectionSql.isDeleted === 1),
				user: (connectionSql.isDeleted === 1),
				password: (connectionSql.isDeleted === 1),
				showPassword: false,
				creationDate: true,
				isDeleted: true,
			})

			setReadonlyStatus({
				id: true,
				name: ((connectionSql.id && connectionSql.id !== null)) ? true : false,
				connectionType: true,
				// connectionType: ((connectionSql.id && connectionSql.id !== null)) ? true : false,
				connectorType: false,
				host: false,
				port: false,
				sid: false,
				serviceName: false,
				databaseName: false,
				user: false,
				password: false,
				showPassword: false,
				creationDate: true,
				isDeleted: true,
			})
		}
	}, [connectionSql, selectConnectionTypeNames, selectConnectorTypeNames, setDisabilityStatus]);

	const handleClickShowPassword = () => {
		setValues({ ...values, showPassword: !values.showPassword });
	};

	const handleMouseDownPassword = (event) => {
		event.preventDefault();
	};

	useEffect(() => {
		if (routeParams.id && routeParams.id != null && routeParams.id==connection.id && connection?.connectionType?.id==1) {
			dispatch(getConnectionSql(routeParams));
		}
		else {
			dispatch(clearSqlConnection(routeParams));
		}
	}, [dispatch,connection, routeParams]);

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
							onBlur={event => changeApply()}
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
							fullWidth={true} onChange={handleChange('host')}
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
				{
					values.connectionType?.id === 1 ?
						(
							<Grid container spacing={3}>

								{
									values.connectorType?.id === 2 ?
										(
											<Grid item xs>
												<TextField
													id="standard-name"
													label="Sid"
													fullWidth={true}
													InputLabelProps={{
														shrink: true,
													}}
													disabled={disabilityStatus.sid}
													readOnly={readonlyStatus.sid}
													value={checkValue(values.sid)}
													onChange={handleChange('sid')}
													onBlur={event => changeApply()}
												/>
											</Grid>
										) : ("")
								}
								{
									values.connectorType?.id === 2 ?
										(

											<Grid item xs>
												<TextField
													id="standard-name"
													label="ServiceName"
													InputLabelProps={{
														shrink: true,
													}}
													disabled={disabilityStatus.serviceName}
													readOnly={readonlyStatus.serviceName}
													value={checkValue(values.serviceName)}
													fullWidth={true}
													onChange={handleChange('serviceName')}
													onBlur={event => changeApply()}
												/>
											</Grid>
										) : ("")
								}
								{
									values.connectorType?.id !== 2 ?
										(
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
										) : ("")
								}
							</Grid>
						) : ("")
				}
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField
							id="standard-name"
							label="User"
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
			</form>
		</React.Fragment >
	);
}
export default ConnectionSqlContent;
