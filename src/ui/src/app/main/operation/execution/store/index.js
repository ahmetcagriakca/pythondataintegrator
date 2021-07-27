import { combineReducers } from '@reduxjs/toolkit';
import dataOperationJobExecution from './dataOperationJobExecutionSlice';
import statusName from './statusNameSlice';

const reducer = combineReducers({
	dataOperationJobExecution,
	statusName,
});

export default reducer;
