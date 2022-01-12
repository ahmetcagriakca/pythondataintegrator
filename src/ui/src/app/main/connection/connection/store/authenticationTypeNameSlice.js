import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getAuthenticationTypeName = createAsyncThunk('connectionApp/authenticationTypeName/getAuthenticationTypeName', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Lookup/AuthenticationType', {
		});
		const data = await response.data;
		return data.result.data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const authenticationTypeNameAdapter = createEntityAdapter({});

export const { selectAll: selectAuthenticationTypeName, selectById: selectAuthenticationTypeNameById } = authenticationTypeNameAdapter.getSelectors(
	state => state.connectionApp.authenticationTypeName
);

const authenticationTypeName = createSlice({
	name: 'connectionApp/authenticationTypeName',
	initialState: authenticationTypeNameAdapter.getInitialState({}),
	reducers: {},
	extraReducers: {
		[getAuthenticationTypeName.fulfilled]: (state, action) => {
			authenticationTypeNameAdapter.setAll(state, action.payload);
		}
	}
});
export default authenticationTypeName.reducer;
