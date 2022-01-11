import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getConnectionBigData = createAsyncThunk('connectionApp/connectionBigData/getConnectionBigData', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Connection/BigDataById', {
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
export const postConnectionBigData = createAsyncThunk('connectionApp/connectionBigData/postConnectionBigData', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/BigData', {
			Name: params.name,
			ConnectorTypeId: params.connectorType.id,
			Host: params.host,
			Port: params.port,
			DatabaseName: params.databaseName,
			AuthenticationType: params.authenticationType.id,
			User: params.user,
			Password: params.password,
			KrbRealm: params.krbRealm,
			KrbFqdn: params.krbFqdn,
			KrbServiceName: params.krbServiceName,
			Ssl: params.ssl,
			UseOnlySspi: params.useOnlySspi,
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const checkBigDataConnection = createAsyncThunk('connectionApp/connectionBigData/checkBigDataConnection', async (params, extra)  => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/CheckBigData', {
			ConnectionName: params.ConnectionName,
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const checkBigDataTableRowCount = createAsyncThunk('connectionApp/connectionBigData/checkBigDataTableRowCount', async (params, extra)  => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Connection/CheckBigDataTableRowCount', {
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


export const clearBigDataConnection = createAsyncThunk('connectionApp/connectionBigData/clearConnection', async (params, extra)  => {
	return {};
});



const connectionBigDataAdapter = createEntityAdapter({});

export const { selectAll: selectConnection, selectById: selectConnectionById } = connectionBigDataAdapter.getSelectors(
	state => state.connectionApp.connectionBigData
);

const connectionBigDataSlice = createSlice({
	name: 'connectionApp/connectionBigData',
	initialState: connectionBigDataAdapter.getInitialState({
		data: {},
	}),
	reducers: {},
	extraReducers: {
		[getConnectionBigData.fulfilled]: (state, action) => {
			connectionBigDataAdapter.setAll(state, [action.payload.result.data]);
			state.data = action.payload.result.data;
		},
		[clearBigDataConnection.fulfilled]: (state, action) => {
			connectionBigDataAdapter.setAll(state, []);
			state.data = {};
		},
	}
});
export default connectionBigDataSlice.reducer;
