import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getConnectionSql = createAsyncThunk('connectionApp/connectionSql/getConnectionSql', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Connection/SqlById', {
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
export const postConnectionSql = createAsyncThunk('connectionApp/connectionSql/postConnectionSql', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/Sql', {
			Name: params.name,
			ConnectorTypeId: params.connectorType.id,
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

export const deleteSqlConnection = createAsyncThunk('connectionApp/connectionSql/deleteConnection', async (params, extra) => {
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



export const checkSqlConnection = createAsyncThunk('connectionApp/connectionSql/checkSqlConnection', async (params, extra)  => {
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

export const checkSqlTableRowCount = createAsyncThunk('connectionApp/connectionSql/checkSqlTableRowCount', async (params, extra)  => {
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


export const clearSqlConnection = createAsyncThunk('connectionApp/connectionSql/clearConnection', async (params, extra)  => {
	return {};
});



const connectionSqlAdapter = createEntityAdapter({});

export const { selectAll: selectConnection, selectById: selectConnectionById } = connectionSqlAdapter.getSelectors(
	state => state.connectionApp.connection
);

const connectionSqlSlice = createSlice({
	name: 'connectionApp/connectionSql',
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
