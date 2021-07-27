import { combineReducers } from '@reduxjs/toolkit';
import dataOperationJob from './dataOperationJobSlice';

const reducer = combineReducers({
	dataOperationJob,
});

export default reducer;
