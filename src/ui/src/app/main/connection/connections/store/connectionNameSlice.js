import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getConnectionName = createAsyncThunk('connectionsApp/connectionName/getConnectionName', async params => {
	// GetConnection
	const response = await axios.get('/api/Lookup/Connection', {
	});
	const data = await response.data;
	return data.result.data;
});

export const connectionNameAdapter = createEntityAdapter({});

export const { selectAll: selectConnectionName, selectById: selectConnectionNameById } = connectionNameAdapter.getSelectors(
	state => state.connectionsApp.connectionName
);

const connectionNameSlice = createSlice({
	name: 'connectionsApp/connectionName',
	initialState: connectionNameAdapter.getInitialState({}),
	reducers: {

	},

	extraReducers: {
		[getConnectionName.fulfilled]: (state, action) => {
			connectionNameAdapter.setAll(state, action.payload);
		}
	}
});

export default connectionNameSlice.reducer;
