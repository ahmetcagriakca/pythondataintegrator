import { combineReducers } from '@reduxjs/toolkit';
import dataOperation from './dataOperationSlice';
import connectionName from './connectionNameSlice';

const reducer = combineReducers({
	dataOperation,
	connectionName,
});

export default reducer;
