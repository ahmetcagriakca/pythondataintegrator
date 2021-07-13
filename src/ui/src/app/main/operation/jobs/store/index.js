import { combineReducers } from '@reduxjs/toolkit';
import dataOperationJobs from './dataOperationJobsSlice';
import dataOperationName from './dataOperationNameSlice';

const reducer = combineReducers({
	dataOperationJobs,
	dataOperationName
});

export default reducer;
