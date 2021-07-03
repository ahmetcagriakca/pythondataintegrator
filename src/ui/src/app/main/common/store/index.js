import { combineReducers } from '@reduxjs/toolkit';
import snackbarReducer from './snackbarSlice';

const reducer = combineReducers({
	snackbar: snackbarReducer
});

export default reducer;
