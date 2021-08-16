import { combineReducers } from '@reduxjs/toolkit';
import connections from './connectionsSlice';
import connectionName from './connectionNameSlice';
import connectionTypeName from './connectionTypeNameSlice';
import connectorTypeName from './connectorTypeNameSlice';

const reducer = combineReducers({
	connections,
	connectionName,
	connectionTypeName,
	connectorTypeName
});

export default reducer;
