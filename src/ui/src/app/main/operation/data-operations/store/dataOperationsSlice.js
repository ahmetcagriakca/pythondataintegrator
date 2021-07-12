import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getDataOperations = createAsyncThunk('dataOperationsApp/dataOperations/getDataOperations', async params => {
	// GetDataOperation
	const response = await axios.get('/api/DataOperation', {
		params: {
			PageNumber: params.PageNumber,
			PageSize: params.PageSize,
			Id: params.DataOperationId,
			OrderBy: params.OrderBy,
			Order: params.Order
		}
	});
	const data = await response.data;
	return data;
});


const dataOperationsAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperations, selectById: selectDataOperationById } = dataOperationsAdapter.getSelectors(
	state => state.dataOperationsApp.dataOperations
);

const dataOperationSlice = createSlice({
	name: 'dataOperationsApp/dataOperations',
	initialState: dataOperationsAdapter.getInitialState({
		count: 0,
		dataOperation: {},
		pageNumber: 1,
		pageSize: 0
	}),
	reducers: {},
	extraReducers: {
		[getDataOperations.fulfilled]: (state, action) => {
			dataOperationsAdapter.setAll(state, action.payload.result.dataOperations);
			state.pageNumber = action.payload.result.pageNumber;
			state.pageSize = action.payload.result.pageSize;
			state.count = action.payload.result.count;
		}
	}
});
export default dataOperationSlice.reducer;
