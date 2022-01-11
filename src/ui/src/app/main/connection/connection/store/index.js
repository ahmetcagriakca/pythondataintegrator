import { combineReducers } from '@reduxjs/toolkit';
import authenticationTypeName from './authenticationTypeNameSlice';
import connection from './connectionSlice';
import connectionSql from './connectionSqlSlice';
import connectionBigData from './connectionBigDataSlice';
import connectionTypeName from './connectionTypeNameSlice';
import connectorTypeName from './connectorTypeNameSlice';

const reducer = combineReducers({
	authenticationTypeName,
	connection,
	connectionSql,
	connectionBigData,
	connectionTypeName,
	connectorTypeName
});

export default reducer;
