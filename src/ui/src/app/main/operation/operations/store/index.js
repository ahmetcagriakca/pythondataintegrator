import { combineReducers } from '@reduxjs/toolkit';
import dataOperations from './dataOperationsSlice';
import dataOperationName from './dataOperationNameSlice';

const reducer = combineReducers({
	dataOperations,
	dataOperationName,
});

export default reducer;
