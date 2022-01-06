import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getConnectionTypeName = createAsyncThunk('connectionSqlApp/connectionTypeName/getConnectionTypeName', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Lookup/ConnectionType', {
		});
		const data = await response.data;
		return data.result.data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const connectionTypeNameAdapter = createEntityAdapter({});

export const { selectAll: selectConnectionTypeName, selectById: selectConnectionTypeNameById } = connectionTypeNameAdapter.getSelectors(
	state => state.connectionSqlApp.connectionTypeName
);

const connectionTypeName = createSlice({
	name: 'connectionSqlApp/connectionTypeName',
	initialState: connectionTypeNameAdapter.getInitialState({}),
	reducers: {},
	extraReducers: {
		[getConnectionTypeName.fulfilled]: (state, action) => {
			connectionTypeNameAdapter.setAll(state, action.payload);
		}
	}
});
export default connectionTypeName.reducer;
