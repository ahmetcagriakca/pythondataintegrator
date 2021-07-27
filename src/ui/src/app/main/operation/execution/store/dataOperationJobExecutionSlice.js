import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getDataOperationJobExecution = createAsyncThunk('dataOperationJobExecutionApp/dataOperationJobExecution/getDataOperationJobExecution', async params => {
	// GetDataOperationJobExecution
	const response = await axios.get('/api/Operation/JobExecutionById', {
		params: {
			Id: params.id
		}
	});
	const data = await response.data;
	return data;
});


const dataOperationJobExecutionAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationJobExecution, selectById: selectDataOperationJobExecutionById } = dataOperationJobExecutionAdapter.getSelectors(
	state => state.dataOperationJobExecutionApp.dataOperationJobExecution
);

const dataOperationJobExecutionlice = createSlice({
	name: 'dataOperationJobExecutionApp/dataOperationJobExecution',
	initialState: dataOperationJobExecutionAdapter.getInitialState({
		dataOperationJobExecution: {},
	}),
	reducers: {},
	extraReducers: {
		[getDataOperationJobExecution.fulfilled]: (state, action) => {
			dataOperationJobExecutionAdapter.setAll(state, [action.payload.result.data]);
		}
	}
});
export default dataOperationJobExecutionlice.reducer;
