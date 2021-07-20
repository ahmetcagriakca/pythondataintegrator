import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getConnectorTypeName = createAsyncThunk('connectionsApp/connectorTypeName/getConnectorTypeName', async params => {
	// GetConnection
	const response = await axios.get('/api/Lookup/ConnectorType', {
	});
	const data = await response.data;
	return data.result.data;
});

export const connectorTypeNameAdapter = createEntityAdapter({});

export const { selectAll: selectConnectorTypeName, selectById: selectConnectorTypeNameById } = connectorTypeNameAdapter.getSelectors(
	state => state.connectionsApp.connectorTypeName
);

const connectorTypeName = createSlice({
	name: 'connectionsApp/connectorTypeName',
	initialState: connectorTypeNameAdapter.getInitialState({}),
	reducers: {},
	extraReducers: {
		[getConnectorTypeName.fulfilled]: (state, action) => {
			connectorTypeNameAdapter.setAll(state, action.payload);
		}
	}
});
export default connectorTypeName.reducer;
