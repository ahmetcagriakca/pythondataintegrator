import React, { useState, useEffect } from "react";
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import { makeStyles } from '@material-ui/core/styles';
import { useDispatch, useSelector } from 'react-redux';
import withReducer from 'app/store/withReducer';
import reducer from './store';
import { initialState } from './store/loadingSlice';

const useStyles = makeStyles(theme => ({
	backdrop: {
		zIndex: theme.zIndex.drawer + 1,
		color: '#fff',
	},
}));

const Loading = () => {
	const classes = useStyles();

	// const openBackdrop = initialState.loading
	const openBackdrop = useSelector(({ loading }) => {
		return loading.loading.loading
	});

	// const [openBackdrop, setOpenBackdrop] = React.useState(true);
	// const handleBackdropClose = () => {
	// 	setOpenBackdrop(false);
	// };
	// const handleToggle = () => {
	// 	setOpenBackdrop(true);
	// };
	return (
		<div>
			<Backdrop className={classes.backdrop} open={openBackdrop} >
				<CircularProgress color="inherit" />
			</Backdrop>
		</div>
	)
}
export default withReducer('loading', reducer)(Loading);