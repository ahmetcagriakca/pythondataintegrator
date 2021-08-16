import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getDataOperationJobExecutionLogs = createAsyncThunk('dataOperationJobExecutionApp/dataOperationJobExecutionLogs/getDataOperationJobExecutionLogs', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Operation/JobExecutionLog', {
			params: {
				ExecutionId: params.ExecutionId
			}
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});


const dataOperationJobExecutionLogsAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationJobExecutionLogs, selectById: selectDataOperationJobExecutionById } = dataOperationJobExecutionLogsAdapter.getSelectors(
	state => state.dataOperationJobExecutionApp.dataOperationJobExecutionLogs
);

const dataOperationJobExecutionLogsSlice = createSlice({
	name: 'dataOperationJobExecutionApp/dataOperationJobExecutionLogs',
	initialState: dataOperationJobExecutionLogsAdapter.getInitialState({
		dataOperationJobExecution: {},
	}),
	reducers: {},
	extraReducers: {
		[getDataOperationJobExecutionLogs.fulfilled]: (state, action) => {
			dataOperationJobExecutionLogsAdapter.setAll(state, action.payload.result.data);
		}
	}
});
export default dataOperationJobExecutionLogsSlice.reducer;
