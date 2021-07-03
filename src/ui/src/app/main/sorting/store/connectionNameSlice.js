import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getConnectionName = createAsyncThunk('connectionApp/connectionName/getConnectionName', async params => {
	const response = await axios.get('api/Lookup/GetConnectionName', {
		params: {
			PageNumber: 1,
			PageSize: 20,
			Name: params.Name
		}
	});
	const data = await response.data;
	return data;
});

const connectionNameAdapter = createEntityAdapter({});

export const { selectAll: selectConnectionName, selectById: selectConnectionNameById } = connectionNameAdapter.getSelectors(
	state => state.connectionApp.connectionName
);

const connectionNameSlice = createSlice({
	name: 'connectionApp/connectionName',
	initialState: connectionNameAdapter.getInitialState({}),
	reducers: {},
	extraReducers: {
		[getConnectionName.fulfilled]: connectionNameAdapter.setAll
	}
});

export default connectionNameSlice.reducer;
