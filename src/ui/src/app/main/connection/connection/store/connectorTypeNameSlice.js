import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getConnectorTypeName = createAsyncThunk('connectionApp/connectorTypeName/getConnectorTypeName', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Lookup/ConnectorType', {
		});
		const data = await response.data;
		return data.result.data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const connectorTypeNameAdapter = createEntityAdapter({});

export const { selectAll: selectConnectorTypeName, selectById: selectConnectorTypeNameById } = connectorTypeNameAdapter.getSelectors(
	state => state.connectionApp.connectorTypeName
);

const connectorTypeName = createSlice({
	name: 'connectionApp/connectorTypeName',
	initialState: connectorTypeNameAdapter.getInitialState({}),
	reducers: {},
	extraReducers: {
		[getConnectorTypeName.fulfilled]: (state, action) => {
			connectorTypeNameAdapter.setAll(state, action.payload);
		}
	}
});
export default connectorTypeName.reducer;
