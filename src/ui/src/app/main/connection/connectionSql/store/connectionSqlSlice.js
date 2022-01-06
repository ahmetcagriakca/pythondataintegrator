import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getConnectionSql = createAsyncThunk('connectionSqlApp/connection/getConnectionSql', async (params, extra) => {
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
export const postConnectionSql = createAsyncThunk('connectionSqlApp/connection/postConnectionSql', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/Sql', {
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

export const deleteSqlConnection = createAsyncThunk('connectionSqlApp/connection/deleteConnection', async (params, extra) => {
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



export const checkSqlConnection = createAsyncThunk('connectionSqlApp/connection/checkSqlConnection', async (params, extra)  => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/CheckSql', {
			ConnectionName: params.ConnectionName,
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const checkSqlTableRowCount = createAsyncThunk('connectionSqlApp/connection/checkSqlTableRowCount', async (params, extra)  => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/CheckSqlTableRowCount', {
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


export const clearSqlConnection = createAsyncThunk('connectionSqlApp/connection/clearConnection', async (params, extra)  => {
	return {};
});



const connectionSqlAdapter = createEntityAdapter({});

export const { selectAll: selectConnection, selectById: selectConnectionById } = connectionSqlAdapter.getSelectors(
	state => state.connectionSqlApp.connection
);

const connectionSqlSlice = createSlice({
	name: 'connectionSqlApp/connection',
	initialState: connectionSqlAdapter.getInitialState({
		data: {},
	}),
	reducers: {},
	extraReducers: {
		[getConnectionSql.fulfilled]: (state, action) => {
			connectionSqlAdapter.setAll(state, [action.payload.result.data]);
			state.data = action.payload.result.data;
		},
		[clearSqlConnection.fulfilled]: (state, action) => {
			connectionSqlAdapter.setAll(state, []);
			state.data = {};
		},
	}
});
export default connectionSqlSlice.reducer;
