import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getConnections = createAsyncThunk('connectionApp/connection/getConnections', async params => {
	// GetConnection
	const response = await axios.get('/api/Connection', {
		params: {
			PageNumber: params.PageNumber,
			PageSize: params.PageSize,
			ConenctionId: params.ConenctionId,
			OrderBy: params.OrderBy,
			Order: params.Order
		}
	});
	const data = await response.data;
	return data;
});

const connectionAdapter = createEntityAdapter({});

export const { selectAll: selectConnections, selectById: selectConnectionById } = connectionAdapter.getSelectors(
	state => state.connectionApp.connection
);

const connectionSlice = createSlice({
	name: 'connectionApp/connections',
	initialState: connectionAdapter.getInitialState({
		count: 0,
		connection: {},
		pageNumber: 0,
		pageSize: 0
	}),
	reducers: {},
	extraReducers: {
		[getConnections.fulfilled]: (state, action) => {
			debugger
			const { connection, count, pageNumber, pageSize } = action.payload;
			connectionAdapter.setAll(state, action.payload.Result);
			state.pageNumber = 1;
			state.pageSize = 10;
			state.count = 10;
		}
	}
});
export default connectionSlice.reducer;
