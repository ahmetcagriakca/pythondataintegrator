import { combineReducers } from '@reduxjs/toolkit';
import connectionSql from './connectionSqlSlice';
import connectionTypeName from './connectionTypeNameSlice';
import connectorTypeName from './connectorTypeNameSlice';

const reducer = combineReducers({
	connectionSql,
	connectionTypeName,
	connectorTypeName
});

export default reducer;
