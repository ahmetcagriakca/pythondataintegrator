import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getDataOperationJobExecutions = createAsyncThunk('dataOperationJobExecutionsApp/dataOperationJobExecutions/getDataOperationJobExecutions', async params => {
	// GetDataOperationJobExecution
	const response = await axios.get('/api/Operation/JobExecution', {
		params: {
			PageNumber: params.PageNumber,
			PageSize: params.PageSize,
			OrderBy: params.OrderBy,
			Order: params.Order,
			DataOperationName: params.DataOperationName,
			OnlyCron: params.OnlyCron,
			StatusId: params.StatusId,
		}
	});
	const data = await response.data;
	return data;
});


const dataOperationJobExecutionsAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationJobExecutions, selectById: selectDataOperationJobExecutionById } = dataOperationJobExecutionsAdapter.getSelectors(
	state => state.dataOperationJobExecutionsApp.dataOperationJobExecutions
);

const dataOperationJobExecutionSlice = createSlice({
	name: 'dataOperationJobExecutionsApp/dataOperationJobExecutions',
	initialState: dataOperationJobExecutionsAdapter.getInitialState({
		count: 0,
		dataOperationJobExecution: {},
		pageNumber: 1,
		pageSize: 0
	}),
	reducers: {},
	extraReducers: {
		[getDataOperationJobExecutions.fulfilled]: (state, action) => {
			dataOperationJobExecutionsAdapter.setAll(state, action.payload.result.data);
			state.pageNumber = action.payload.result.pageNumber;
			state.pageSize = action.payload.result.pageSize;
			state.count = action.payload.result.count;
		}
	}
});
export default dataOperationJobExecutionSlice.reducer;
