import { combineReducers } from '@reduxjs/toolkit';
import connectionBigData from './connectionBigDataSlice';
import connectionTypeName from './connectionTypeNameSlice';
import connectorTypeName from './connectorTypeNameSlice';
import authenticationTypeName from './authenticationTypeNameSlice';

const reducer = combineReducers({
	connectionBigData,
	connectionTypeName,
	connectorTypeName,
	authenticationTypeName
});

export default reducer;
