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
import Icon from '@material-ui/core/Icon';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import Box from '@material-ui/core/Box';


function DataOperationJobsFilterForm(props) {
	const dispatch = useDispatch();
	const classes = filterFormStyles();
	const filterOptions = createFilterOptions({
		matchFrom: 'any',
		stringify: option => {
			return option.name
		},
	});

	const { DataOperationId } = props;

	const isDataOperation = (DataOperationId && DataOperationId !== null && DataOperationId !== 0)
	const routeParams = useParams();
	routeParams.DataOperationId = isDataOperation ? DataOperationId : null;
	useEffect(() => {
		dispatch(getDataOperationName(routeParams));
	}, [dispatch, routeParams]);

	//states
	const [dataOperation, setDataOperation] = React.useState(null);
	const selectDataOperationNames = useSelector(selectDataOperationName);

	const [onlyCron, setOnlyCron] = React.useState(isDataOperation ? false : true);
	const handleOnlyCronChange = (event) => {
		setOnlyCron(event.target.checked);
	};

	const [onlyUndeleted, setOnlyUndeleted] = React.useState(isDataOperation ? false : true);
	const handleOnlyUndeletedChange = (event) => {
		setOnlyUndeleted(event.target.checked);
	};

	const clear = event => {
		setDataOperation(null);
		setOnlyCron(isDataOperation ? false : true);
		setOnlyUndeleted(isDataOperation ? false : true);

		routeParams.OrderBy = "DataOperationJob.Id";
		routeParams.PageNumber = 1;
		routeParams.Order = null;
		routeParams.DataOperationName = null;
		routeParams.OnlyCron = isDataOperation ? false : true;
		routeParams.OnlyUndeleted = isDataOperation ? false : true;
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

		<Box>
			<Grid container spacing={3}>
				{
					!isDataOperation ?
						(
							<Grid item xs>
								<Autocomplete
									id="country-select-demo"
									style={{ width: '100%' }}
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
											label="Data Operation "
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
						<FormControlLabel style={{ margin: "5px" }}
							control={<Checkbox checked={onlyCron} onChange={handleOnlyCronChange} name="onlyCron" />}
							label="Only Cron"
						/>
					</FormGroup>
				</Grid>
				<Grid item xs>
					<FormGroup row>
						<FormControlLabel style={{ margin: "5px" }}
							control={<Checkbox checked={onlyUndeleted} onChange={handleOnlyUndeletedChange} name="onlyUndeleted" />}
							label="Only Undeleted"
						/>
					</FormGroup>
				</Grid>
				<Grid item xs></Grid>

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
		</Box >
	);
}
export default DataOperationJobsFilterForm;
