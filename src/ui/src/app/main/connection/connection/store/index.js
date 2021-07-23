import { combineReducers } from '@reduxjs/toolkit';
import connection from './connectionSlice';
import connectionTypeName from './connectionTypeNameSlice';
import connectorTypeName from './connectorTypeNameSlice';

const reducer = combineReducers({
	connection,
	connectionTypeName,
	connectorTypeName
});

export default reducer;
