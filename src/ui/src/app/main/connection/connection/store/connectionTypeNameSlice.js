import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getConnectionTypeName = createAsyncThunk('connectionApp/connectionTypeName/getConnectionTypeName', async params => {
	const response = await axios.get('/api/Lookup/ConnectionType', {
	});
	const data = await response.data;
	return data.result.data;
});

export const connectionTypeNameAdapter = createEntityAdapter({});

export const { selectAll: selectConnectionTypeName, selectById: selectConnectionTypeNameById } = connectionTypeNameAdapter.getSelectors(
	state => state.connectionApp.connectionTypeName
);

const connectionTypeName = createSlice({
	name: 'connectionApp/connectionTypeName',
	initialState: connectionTypeNameAdapter.getInitialState({}),
	reducers: {},
	extraReducers: {
		[getConnectionTypeName.fulfilled]: (state, action) => {
			connectionTypeNameAdapter.setAll(state, action.payload);
		}
	}
});
export default connectionTypeName.reducer;
