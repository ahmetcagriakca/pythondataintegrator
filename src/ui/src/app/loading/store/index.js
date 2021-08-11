import { combineReducers } from '@reduxjs/toolkit';
import loading from './loadingSlice';

const loadingReducers = combineReducers({
	loading,
});

export default loadingReducers;
