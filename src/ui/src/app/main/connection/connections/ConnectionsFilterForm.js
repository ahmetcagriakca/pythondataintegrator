import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import { getConnectionName, selectConnectionName } from './store/connectionNameSlice';
import { getConnectionTypeName, selectConnectionTypeName } from './store/connectionTypeNameSlice';
import { getConnectorTypeName, selectConnectorTypeName } from './store/connectorTypeNameSlice';
import { getConnections } from './store/connectionsSlice';
import Button from '@material-ui/core/Button';

import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
const filterOptions = createFilterOptions({
	matchFrom: 'start',
	stringify: option => {
		return option.name
	},
});

const useStyles = makeStyles(theme => ({
	root: {
		flexGrow: 1,
	},
	paper: {
		padding: theme.spacing(2),
		textAlign: 'center',
		color: theme.palette.text.secondary,
	},
	margin: {
		margin: theme.spacing(1)
	},
	extendedIcon: {
		marginRight: theme.spacing(1)
	},
	filterFormClass: {
		background: `linear-gradient(to left, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`,
		color: theme.palette.getContrastText(theme.palette.primary.main)
	},
	autocompleteStyle: {
		borderColor: 'red',
		color: 'red'
	},
	button: {
		margin: theme.spacing(1),
	},
}));

function ConnectionsFilterFom() {
	const classes = useStyles();

	const dispatch = useDispatch();

	const [connection, setConnection] = React.useState(null);
	const [connectionType, setConnectionType] = React.useState(null);
	const [connectorType, setConnectorType] = React.useState(null);
	const selectConnectionNames = useSelector(selectConnectionName);
	const selectConnectionTypeNames = useSelector(selectConnectionTypeName);
	const selectConnectorTypeNames = useSelector(selectConnectorTypeName);

	const routeParams = useParams();


	useEffect(() => {
		dispatch(getConnectionName(routeParams));
	}, [dispatch,routeParams]);
	useEffect(() => {
		dispatch(getConnectionTypeName(routeParams));
	}, [dispatch,routeParams]);
	useEffect(() => {
		dispatch(getConnectorTypeName(routeParams));
	}, [dispatch,routeParams]);


	const clear = event => {
		setConnection(null);
		setConnectionType(null);
		setConnectorType(null);

		routeParams.ConnectionId = null;
		routeParams.ConnectionTypeId = null;
		routeParams.ConnectorTypeId = null;
		routeParams.OrderBy = "Connection.Id";
		routeParams.PageNumber = 1;
		routeParams.Order = null;
		dispatch(getConnections(routeParams));
	};

	const filter = event => {

		let connectionId = null;
		if (connection != null) {
			connectionId = connection.id;
		}
		routeParams.ConnectionId = connectionId;
		let connectionTypeId = null;
		if (connectionType != null) {
			connectionTypeId = connectionType.id;
		}
		routeParams.ConnectionTypeId = connectionTypeId;

		let connectorTypeId = null;
		if (connectorType != null) {
			connectorTypeId = connectorType.id;
		}
		routeParams.ConnectorTypeId = connectorTypeId;
		routeParams.PageNumber = 1;
		dispatch(getConnections(routeParams));
	};




	return (

		<div className={classes.root}
			style={{ padding: '15px 40px 15px 40px' }}
		>
			<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>
			<Grid container spacing={3}>
				<Grid item xs>
					<Autocomplete
						id="country-select-demo"
						style={{ width: 300 }}
						value={connection}
						onChange={(event, newValue) => {
							setConnection(newValue);
						}}
						options={selectConnectionNames}
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
								label="Choose a connection "
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
						value={connectionType}
						onChange={(event, newValue) => {
							setConnectionType(newValue);
						}}
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
						value={connectorType}
						onChange={(event, newValue) => {
							setConnectorType(newValue);
						}}
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
				<Grid item xs></Grid>
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
						className={classes.button}
						// startIcon={<SearchIcon />}
						onClick={filter}
					>
						Search
					</Button>
				</Grid>
			</Grid>
		</div>
	);
}
export default ConnectionsFilterFom;
