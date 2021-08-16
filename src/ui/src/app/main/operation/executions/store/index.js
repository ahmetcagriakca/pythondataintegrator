import { combineReducers } from '@reduxjs/toolkit';
import dataOperationJobExecutions from './dataOperationJobExecutionsSlice';
import dataOperationName from './dataOperationNameSlice';
import statusName from './statusNameSlice';

const reducer = combineReducers({
	dataOperationJobExecutions,
	dataOperationName,
	statusName,
});

export default reducer;
