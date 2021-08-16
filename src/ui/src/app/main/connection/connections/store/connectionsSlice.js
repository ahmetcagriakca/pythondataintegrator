import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getConnections = createAsyncThunk('connectionsApp/connections/getConnections', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Connection', {
			params: {
				PageNumber: params.PageNumber,
				PageSize: params.PageSize,
				OrderBy: params.OrderBy,
				Order: params.Order,
				Id: params.ConnectionId,
				ConnectionTypeId: params.ConnectionTypeId,
				ConnectorTypeId: params.ConnectorTypeId,
				OnlyUndeleted: params.OnlyUndeleted,
			}
		});
		const data = await response.data;
		return data;
	} 
	finally{
		extra.dispatch(setLoading(false))
	}
});

export const checkDatabaseConnection = createAsyncThunk('connectionsApp/connections/checkDatabaseConnection', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/CheckDatabase', {
			ConnectionName: params.ConnectionName,
		});
		const data = await response.data;
		return data;
	} 
	finally{
		extra.dispatch(setLoading(false))
	}
});

const connectionsAdapter = createEntityAdapter({});

export const { selectAll: selectConnections, selectById: selectConnectionById } = connectionsAdapter.getSelectors(
	state => state.connectionsApp.connections
);

const connectionSlice = createSlice({
	name: 'connectionsApp/connections',
	initialState: connectionsAdapter.getInitialState({
		count: 0,
		data: {},
		pageNumber: 1,
		pageSize: 0
	}),
	reducers: {},
	extraReducers: {
		[getConnections.fulfilled]: (state, action) => {
			connectionsAdapter.setAll(state, action.payload.result.data);
			state.data = action.payload.result.pageNumber;
			state.pageNumber = action.payload.result.pageNumber;
			state.pageSize = action.payload.result.pageSize;
			state.count = action.payload.result.count;
		}
	}
});
export default connectionSlice.reducer;
