import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getConnectionName, selectConnectionName } from './store/connectionNameSlice';
import { getConnectionTypeName, selectConnectionTypeName } from './store/connectionTypeNameSlice';
import { getConnectorTypeName, selectConnectorTypeName } from './store/connectorTypeNameSlice';
import { getConnections } from './store/connectionsSlice';
import Button from '@material-ui/core/Button';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Icon from '@material-ui/core/Icon';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Box from '@material-ui/core/Box';



function ConnectionsFilterFom() {
	const dispatch = useDispatch();
	const classes = filterFormStyles();
	const filterOptions = createFilterOptions({
		matchFrom: 'any',
		stringify: option => {
			return option.name
		},
	});

	const [connection, setConnection] = React.useState(null);
	const [connectionType, setConnectionType] = React.useState(null);
	const [connectorType, setConnectorType] = React.useState(null);
	const selectConnectionNames = useSelector(selectConnectionName);
	const selectConnectionTypeNames = useSelector(selectConnectionTypeName);
	const selectConnectorTypeNames = useSelector(selectConnectorTypeName);

	const [onlyUndeleted, setOnlyUndeleted] = React.useState(true);
	const handleOnlyUndeletedChange = (event) => {
		setOnlyUndeleted(event.target.checked);
	};

	const routeParams = useParams();

	useEffect(() => {
		dispatch(getConnectionName(routeParams));
	}, [dispatch, routeParams]);
	useEffect(() => {
		dispatch(getConnectionTypeName(routeParams));
	}, [dispatch, routeParams]);
	useEffect(() => {
		dispatch(getConnectorTypeName(routeParams));
	}, [dispatch, routeParams]);

	const clear = event => {
		setConnection(null);
		setConnectionType(null);
		setConnectorType(null);
		setOnlyUndeleted(true);

		routeParams.ConnectionId = null;
		routeParams.ConnectionTypeId = null;
		routeParams.ConnectorTypeId = null;
		routeParams.OrderBy = "Connection.Id";
		routeParams.PageNumber = 1;
		routeParams.Order = null;
		routeParams.OnlyUndeleted = true;
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
		routeParams.OnlyUndeleted = onlyUndeleted;
		routeParams.PageNumber = 1;
		dispatch(getConnections(routeParams));
	};

	return (
		<Box>
			<Grid container spacing={3}>
				<Grid item xs>
					<Autocomplete
						id="country-select-demo"
						style={{ width: '100%' }}
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
								label="Connection "
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
						style={{ width: '100%' }}
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
								label="Connection type"
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
						style={{ width: '100%' }}
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
								label="Connector type"
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
					<FormControlLabel style={{ margin: "5px" }}
						control={<Checkbox checked={onlyUndeleted} onChange={handleOnlyUndeletedChange} name="onlyUndeleted" />}
						label="Only Undeleted"
					/>
				</Grid>
			</Grid>

			<Box
				component="span"
				m={1} //margin
				className={`${classes.bottomRightBox} ${classes.box}`}
			>
				<ButtonGroup aria-label="outlined primary button group">
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
						color="secondary"
						size="large"
						className={classes.button}
						startIcon={<Icon >search</Icon>}
						onClick={filter}
					>
						Search
					</Button>
				</ButtonGroup>
			</Box>
		</Box>
	);
}
export default ConnectionsFilterFom;
