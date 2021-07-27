import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getDataOperationName, selectDataOperationName } from './store/dataOperationNameSlice';
import { getDataOperationJobs } from './store/dataOperationJobsSlice';
import Button from '@material-ui/core/Button';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { filterFormStyles } from '../../common/styles/FilterFormStyles';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';


function DataOperationJobsFilterForm(props) {
	const dispatch = useDispatch();
	const classes = filterFormStyles();
	const filterOptions = createFilterOptions({
		matchFrom: 'start',
		stringify: option => {
			return option.name
		},
	});

	const isDataOperation = () => (props.DataOperationId && props.DataOperationId !== null && props.DataOperationId !== 0)
	const routeParams = useParams();
	routeParams.DataOperationId = isDataOperation() ? props.DataOperationId : null;
	useEffect(() => {
		dispatch(getDataOperationName(routeParams));
	}, [dispatch, routeParams]);

	//states
	const [dataOperation, setDataOperation] = React.useState(null);
	const selectDataOperationNames = useSelector(selectDataOperationName);

	const [onlyCron, setOnlyCron] = React.useState(isDataOperation() ? false :true);
	const handleOnlyCronChange = (event) => {
		setOnlyCron(event.target.checked);
	};

	const [onlyUndeleted, setOnlyUndeleted] = React.useState(isDataOperation() ? false :true);
	const handleOnlyUndeletedChange = (event) => {
		setOnlyUndeleted(event.target.checked);
	};

	const clear = event => {
		setDataOperation(null);
		setOnlyCron(isDataOperation() ? false : true);
		setOnlyUndeleted(isDataOperation() ? false : true);

		routeParams.OrderBy = "DataOperationJob.Id";
		routeParams.PageNumber = 1;
		routeParams.Order = null;
		routeParams.DataOperationName = null;
		routeParams.OnlyCron = isDataOperation() ? false : true;
		routeParams.OnlyUndeleted = isDataOperation() ? false : true;
		dispatch(getDataOperationJobs(routeParams));
	};

	const filter = event => {
		let dataOperationName = null;
		if (dataOperation != null) {
			dataOperationName = dataOperation.name;
		}
		routeParams.DataOperationName = dataOperationName;

		routeParams.OnlyCron = onlyCron;
		routeParams.OnlyUndeleted = onlyUndeleted;


		routeParams.PageNumber = 1;
		dispatch(getDataOperationJobs(routeParams));
	};

	return (

		<div className={classes.root}
			style={{ padding: '15px 40px 15px 40px' }}
		>
			<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>
			<Grid container spacing={3}>
				{
					!isDataOperation() ?
						(
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
											label="Choose a Data Operation "
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
						) : ("")
				}
				<Grid item xs>

					<FormGroup row>
						<FormControlLabel
							control={<Checkbox checked={onlyCron} onChange={handleOnlyCronChange} name="onlyCron" />}
							label="Only Cron"
						/>
					</FormGroup>
				</Grid>
				<Grid item xs>
					<FormGroup row>
						<FormControlLabel
							control={<Checkbox checked={onlyUndeleted} onChange={handleOnlyUndeletedChange} name="onlyUndeleted" />}
							label="Only Undeleted"
						/>
					</FormGroup>
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
export default DataOperationJobsFilterForm;
