import { combineReducers } from '@reduxjs/toolkit';
import login from './loginSlice';
import user from './userSlice';

const authReducers = combineReducers({
	user,
	login,
});

export default authReducers;
