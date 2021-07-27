import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getDataOperation = createAsyncThunk('dataOperationApp/dataOperation/getDataOperation', async params => {
	// GetDataOperation
	const response = await axios.get('/api/Operation/ById', {
		params: {
			Id: params.id,
		}
	});
	const data = await response.data;
	return data;
});

export const postOperation = createAsyncThunk('dataOperationApp/dataOperation/postOperation', async operationData => {
	// GetConnection
	const response = await axios.post('/api/Operation',operationData);
	const data = await response.data;
	return data;
});


const dataOperationAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperations, selectById: selectDataOperationById } = dataOperationAdapter.getSelectors(
	state => state.dataOperationApp.dataOperation
);

const dataOperationSlice = createSlice({
	name: 'dataOperationApp/dataOperation',
	initialState: dataOperationAdapter.getInitialState({
		dataOperation: {},
	}),
	reducers: {},
	extraReducers: {
		[getDataOperation.fulfilled]: (state, action) => {
			dataOperationAdapter.setAll(state, [action.payload.result.data]);
		}
	}
});
export default dataOperationSlice.reducer;
