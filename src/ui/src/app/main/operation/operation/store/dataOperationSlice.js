import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getOperation = createAsyncThunk('dataOperationApp/dataOperation/getOperation', async params => {
	const response = await axios.get('/api/Operation/ById', {
		params: {
			Id: params.id,
		}
	});
	const data = await response.data;
	return data;
});

export const postOperation = createAsyncThunk('dataOperationApp/dataOperation/postOperation', async operationData => {
	const response = await axios.post('/api/Operation',operationData);
	const data = await response.data;
	return data;
});

export const deleteOperation = createAsyncThunk('dataOperationApp/dataOperation/deleteOperation', async params => {
	const response = await axios.delete('/api/Operation', {
		data: {
			Id: params.id,
		}

	});
	const data = await response.data;
	return data;
});


export const clearOperation = createAsyncThunk('dataOperationApp/dataOperation/clearOperation', async params => {
	return {};
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
