import { combineReducers } from '@reduxjs/toolkit';
import dataOperationJob from './dataOperationJobSlice';
import dataOperationName from './dataOperationNameSlice';

const reducer = combineReducers({
	dataOperationJob,
	dataOperationName,
});

export default reducer;
