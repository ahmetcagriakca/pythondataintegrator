import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getDataOperationJobExecutionIntegrations = createAsyncThunk('dataOperationJobExecutionApp/dataOperationJobExecutionIntegrations/getDataOperationJobExecutionIntegrations', async params => {
	// GetDataOperationJobExecution
	const response = await axios.get('/api/Operation/JobExecutionIntegration', {
		params: {
			ExecutionId: params.ExecutionId
		}
	});
	const data = await response.data;
	return data;
});


const dataOperationJobExecutionIntegrationsAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationJobExecutionIntegrations, selectById: selectDataOperationJobExecutionById } = dataOperationJobExecutionIntegrationsAdapter.getSelectors(
	state => state.dataOperationJobExecutionApp.dataOperationJobExecutionIntegrations
);

const dataOperationJobExecutionIntegrationsSlice = createSlice({
	name: 'dataOperationJobExecutionApp/dataOperationJobExecutionIntegrations',
	initialState: dataOperationJobExecutionIntegrationsAdapter.getInitialState({
		dataOperationJobExecution: {},
	}),
	reducers: {},
	extraReducers: {
		[getDataOperationJobExecutionIntegrations.fulfilled]: (state, action) => {
			dataOperationJobExecutionIntegrationsAdapter.setAll(state, action.payload.result.data);
		}
	}
});
export default dataOperationJobExecutionIntegrationsSlice.reducer;
