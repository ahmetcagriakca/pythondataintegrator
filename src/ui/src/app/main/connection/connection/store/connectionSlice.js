import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getConnection = createAsyncThunk('connectionApp/connection/getConnection', async params => {
	// GetConnection
	const response = await axios.get('/api/Connection', {
		params: {
			Id: params.id,
		}
	});
	const data = await response.data;
	return data;
});
export const updateConnection = createAsyncThunk('connectionApp/connection/updateConnection', async params => {
	// GetConnection
	const response = await axios.post('/api/Connection/Database', {
			Name: params.name,
			ConnectorTypeName: params.connectorType.name,
			Host: params.host,
			Port: params.port,
			Sid: params.sid,
			ServiceName: params.serviceName,
			DatabaseName: params.databaseName,
			User: params.user,
			Password: params.password,
	});
	const data = await response.data;
	return data;
});

export const checkConnection = createAsyncThunk('connectionApp/connection/checkConnection', async params => {
	// GetConnection
	const response = await axios.post('/api/Connection/CheckDatabase', "ConnectionName="+params.name);
	const data = await response.data;
	return data;
});


const connectionAdapter = createEntityAdapter({});

export const { selectAll: selectConnection, selectById: selectConnectionById } = connectionAdapter.getSelectors(
	state => state.connectionApp.connection
);

const connectionSlice = createSlice({
	name: 'connectionApp/connection',
	initialState: connectionAdapter.getInitialState({
		connection: {},
	}),
	reducers: {},
	extraReducers: {
		[getConnection.fulfilled]: (state, action) => {
			connectionAdapter.setAll(state, action.payload.result.data);
			state.connection = action.payload.result.data;
		},
		[updateConnection.fulfilled]: connectionAdapter.addOne
	}
});
export default connectionSlice.reducer;
