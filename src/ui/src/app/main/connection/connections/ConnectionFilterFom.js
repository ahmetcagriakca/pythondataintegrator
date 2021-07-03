import React, { useEffect } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import clsx from 'clsx';

import { makeStyles } from '@material-ui/core/styles';
import { getConnectionName, selectConnectionName } from './store/connectionNameSlice';
import { getConnections } from './store/connectionSlice';


const useStyles = makeStyles(theme => ({
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
	}
}));

function ConnectionFilterFom() {
	const classes = useStyles();

	const dispatch = useDispatch();
	const selectConnectionNames = useSelector(selectConnectionName);
	const [monitoringStatus, setMonitoringStatusValue] = React.useState([]);

	const routeParams = useParams();
	routeParams.PageNumber = 1;
	routeParams.PageSize = 20;


	useEffect(() => {
		dispatch(getConnectionName(routeParams));
	}, [dispatch]);

	const ConnectionNameFilter = event => {
		routeParams.Name = event;
		dispatch(getConnectionName(routeParams));
	};

	const handleChangePage = (event, newPage) => {
		routeParams.PageNumber = 100;
	};


	const selectedConnection = (event, selectedValue) => {
		routeParams.ConnectionId = null;
		if (selectedValue != null) {
			const selectedConnectionName = selectedValue.name;
			const selectedConnectionId = selectedValue.id;
			routeParams.ConnectionId = selectedConnectionId;
		}
		dispatch(getConnections(routeParams));
	};



	return (
		<div
			className={clsx('flex flex-col flex-1 max-w-2x2 w-full mx-auto px-8 sm:px-32')}
			style={{ padding: '15px 40px 15px 40px' }}
		>
			<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10">
				<Grid container spacing={10}>
					<Grid item sm={3}>
						<Autocomplete
							id="combo-box-demo"
							options={selectConnectionNames}
							getOptionLabel={option => option.name}
							renderInput={params => <TextField {...params} label="Connection Name" variant="outlined" />}
							onChange={(event, newValue) => {
								se(event, newValue);
							}}
							onInputChange={(event, newInputValue) => {
								ConnectionNameFilter(newInputValue);
							}}
							fullWidth
						/>
					</Grid>
				</Grid>
			</div>
		</div>
	);
}

export default ConnectionFilterFom;
