import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getConnection, updateConnection, checkConnection } from './store/connectionSlice';
import { getConnectionTypeName, selectConnectionTypeName } from './store/connectionTypeNameSlice';
import { getConnectorTypeName, selectConnectorTypeName } from './store/connectorTypeNameSlice';
import Button from '@material-ui/core/Button';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';


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
		name: '',
		connectionType: null,
		connectorType: null,
		host: '',
		port: 0,
		sid: '',
		serviceName: '',
		databaseName: '',
		user: '',
		password: ''
	});

	const handleChange = (prop) => (event) => {
		setValues({ ...values, [prop]: event.target.value });
	};

	const selectConnectionTypeNames = useSelector(selectConnectionTypeName);
	const selectConnectorTypeNames = useSelector(selectConnectorTypeName);

	const routeParams = useParams();

	const connection = useSelector(({ connectionApp }) => {
		return connectionApp.connection.entities[routeParams.id]
	});

	useEffect(() => {
		dispatch(getConnectionTypeName(routeParams));
		dispatch(getConnectorTypeName(routeParams));
		dispatch(getConnection(routeParams));
	}, [dispatch, routeParams]);

	useEffect(() => {
		if (connection && connection != null) {
			setValues(connection);
		}
	}, [connection, selectConnectionTypeNames, selectConnectorTypeNames]);

	const save = event => {
		dispatch(updateConnection(values));
	};

	const check = event => {
		routeParams.name = values.name
		dispatch(checkConnection(routeParams));
	};

	return (

		<div className={classes.root}
			style={{ padding: '15px 40px 15px 40px' }}
		>
			<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>

			<form className={classes.root} noValidate autoComplete="off">
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="standard-name" label="Name" value={values.name} onChange={handleChange('name')} />
					</Grid>
					<Grid item xs>
						<Autocomplete
							id="country-select-demo"
							style={{ width: 300 }}
							value={values.connectionType}
							onChange={handleChange('connectionType')}
							options={selectConnectionTypeNames}
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
									label="Choose a connection type"
									variant="outlined"
									inputProps={{
										...params.inputProps,
										autoComplete: 'new-password', // disable autocomplete and autofill
									}}
								/>
							)}
							autoHighlight
							clearOnEscape
							openOnFocus
						/>
					</Grid>
					<Grid item xs>
						<Autocomplete
							id="country-select-demo"
							style={{ width: 300 }}
							value={values.connectorType}
							onChange={handleChange('connectorType')}
							options={selectConnectorTypeNames}
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
									label="Choose a connector type"
									variant="outlined"
									inputProps={{
										...params.inputProps,
										autoComplete: 'new-password', // disable autocomplete and autofill
									}}
								/>
							)}
							autoHighlight
							clearOnEscape
							openOnFocus
						/>

					</Grid>
					<Grid item xs>
						<TextField id="standard-name" label="Host" value={values.host} onChange={handleChange('host')} />
					</Grid>
				</Grid>
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="standard-name" label="Port" value={values.port} onChange={handleChange('port')} />
					</Grid>
					<Grid item xs>
						<TextField id="standard-name" label="Sid" value={values.sid} onChange={handleChange('sid')} />
					</Grid>
					<Grid item xs>
						<TextField id="standard-name" label="ServiceName" value={values.serviceName} onChange={handleChange('serviceName')} />
					</Grid>
					<Grid item xs>
						<TextField id="standard-name" label="DatabaseName" value={values.databaseName} onChange={handleChange('databaseName')} />
					</Grid>
				</Grid>
				<Grid container spacing={3}>
					<Grid item xs>
						<TextField id="standard-name" label="User" value={values.user} onChange={handleChange('user')} />
					</Grid>
					<Grid item xs>
						<TextField id="standard-name" label="Password" value={values.password}
							type="password" onChange={handleChange('password')} />
					</Grid>
					<Grid item xs>
					</Grid>
					<Grid item xs>
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
							className={classes.button}
							// startIcon={<SearchIcon />}
							onClick={check}
						>
							Check Connection
						</Button>
					</Grid>
					<Grid item xs={1}>
						<Button
							variant="contained"
							color="secondary"
							size="large"
							className={classes.button}
							// startIcon={<SearchIcon />}
							onClick={save}
						>
							Save
						</Button>
					</Grid>
				</Grid>
			</form>
		</div>
	);
}
export default ConnectionContent;
