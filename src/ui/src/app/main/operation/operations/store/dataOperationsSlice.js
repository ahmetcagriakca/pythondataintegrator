import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getDataOperations = createAsyncThunk('dataOperationsApp/dataOperations/getDataOperations', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Operation', {
			params: {
				PageNumber: params.PageNumber,
				PageSize: params.PageSize,
				OrderBy: params.OrderBy,
				Order: params.Order,
				DataOperationName: params.DataOperationName,
				OnlyUndeleted: params.OnlyUndeleted,
			}
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
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
			dataOperationsAdapter.setAll(state, action.payload.result.data);
			state.pageNumber = action.payload.result.pageNumber;
			state.pageSize = action.payload.result.pageSize;
			state.count = action.payload.result.count;
		}
	}
});
export default dataOperationSlice.reducer;
