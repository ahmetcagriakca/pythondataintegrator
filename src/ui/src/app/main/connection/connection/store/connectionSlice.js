import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getConnection = createAsyncThunk('connectionApp/connection/getConnection', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Connection/ById', {
			params: {
				Id: params.id,
			}
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});
export const postConnection = createAsyncThunk('connectionApp/connection/postConnection', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
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
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const deleteConnection = createAsyncThunk('connectionApp/connection/deleteConnection', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.delete('/api/Connection', {
			data: {
				Id: params.id,
			}

		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});



export const checkDatabaseConnection = createAsyncThunk('connectionApp/connection/checkDatabaseConnection', async (params, extra)  => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/CheckDatabase', {
			ConnectionName: params.ConnectionName,
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const checkDatabaseTableRowCount = createAsyncThunk('connectionApp/connection/checkDatabaseTableRowCount', async (params, extra)  => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/CheckDatabaseTableRowCount', {
			ConnectionName: params.ConnectionName,
			Schema: params.Schema,
			Table: params.Table,
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});


export const clearConnection = createAsyncThunk('connectionApp/connection/clearConnection', async (params, extra)  => {
	return {};
});



const connectionAdapter = createEntityAdapter({});

export const { selectAll: selectConnection, selectById: selectConnectionById } = connectionAdapter.getSelectors(
	state => state.connectionApp.connection
);

const connectionSlice = createSlice({
	name: 'connectionApp/connection',
	initialState: connectionAdapter.getInitialState({
		data: {},
	}),
	reducers: {},
	extraReducers: {
		[getConnection.fulfilled]: (state, action) => {
			connectionAdapter.setAll(state, [action.payload.result.data]);
			state.data = action.payload.result.data;
		},
		[clearConnection.fulfilled]: (state, action) => {
			connectionAdapter.setAll(state, []);
			state.data = {};
		},
	}
});
export default connectionSlice.reducer;
