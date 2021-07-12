import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import { getDataOperationName, selectDataOperationName } from './store/dataOperationNameSlice';
import { getDataOperations } from './store/dataOperationsSlice';
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

function DataOperationsFilterFom() {
	const classes = useStyles();

	const dispatch = useDispatch();

	const [dataOperation, setDataOperation] = React.useState(null);
	const selectDataOperationNames = useSelector(selectDataOperationName);

	const routeParams = useParams();


	useEffect(() => {
		dispatch(getDataOperationName(routeParams));
	}, [dispatch,routeParams]);
	const clear = event => {
		setDataOperation(null);

		routeParams.DataOperationId = null;
		routeParams.OrderBy = "DataOperation.Id";
		routeParams.PageNumber = 1;
		routeParams.Order = null;
		dispatch(getDataOperations(routeParams));
	};

	const filter = event => {

		let dataOperationId = null;
		if (dataOperation != null) {
			dataOperationId = dataOperation.id;
		}
		routeParams.DataOperationId = dataOperationId;

		routeParams.PageNumber = 1;
		dispatch(getDataOperations(routeParams));
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
						value={dataOperation}
						onChange={(event, newValue) => {
							setDataOperation(newValue);
						}}
						options={selectDataOperationNames}
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
								label="Choose a dataOperation "
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
export default DataOperationsFilterFom;
