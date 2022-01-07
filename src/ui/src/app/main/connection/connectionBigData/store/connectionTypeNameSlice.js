import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getConnectionTypeName = createAsyncThunk('connectionBigDataApp/connectionTypeName/getConnectionTypeName', async (params, extra) => {
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
	state => state.connectionBigDataApp.connectionTypeName
);

const connectionTypeName = createSlice({
	name: 'connectionBigDataApp/connectionTypeName',
	initialState: connectionTypeNameAdapter.getInitialState({}),
	reducers: {},
	extraReducers: {
		[getConnectionTypeName.fulfilled]: (state, action) => {
			connectionTypeNameAdapter.setAll(state, action.payload);
		}
	}
});
export default connectionTypeName.reducer;
