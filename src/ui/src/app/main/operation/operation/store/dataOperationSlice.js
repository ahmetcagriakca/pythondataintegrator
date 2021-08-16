import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getOperation = createAsyncThunk('dataOperationApp/dataOperation/getOperation', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Operation/ById', {
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

export const postOperation = createAsyncThunk('dataOperationApp/dataOperation/postOperation', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Operation', params);
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const deleteOperation = createAsyncThunk('dataOperationApp/dataOperation/deleteOperation', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.delete('/api/Operation', {
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


export const clearOperation = createAsyncThunk('dataOperationApp/dataOperation/clearOperation', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		return {};
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});


const dataOperationAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperations, selectById: selectDataOperationById } = dataOperationAdapter.getSelectors(
	state => state.dataOperationApp.dataOperation
);

const dataOperationSlice = createSlice({
	name: 'dataOperationApp/dataOperation',
	initialState: dataOperationAdapter.getInitialState({
		data: {},
	}),
	reducers: {},
	extraReducers: {
		[getOperation.fulfilled]: (state, action) => {
			dataOperationAdapter.setAll(state, [action.payload.result.data]);
			state.data = action.payload.result.data;
		},
		[clearOperation.fulfilled]: (state, action) => {
			dataOperationAdapter.setAll(state, []);
			state.data = {};
		},
	}
});
export default dataOperationSlice.reducer;
