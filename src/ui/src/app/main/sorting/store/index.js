import { combineReducers } from '@reduxjs/toolkit';
import connection from './connectionSlice';
import connectionName from './connectionNameSlice';

const reducer = combineReducers({
	connection,
	connectionName
});

export default reducer;
