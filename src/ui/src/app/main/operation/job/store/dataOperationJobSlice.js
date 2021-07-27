import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getDataOperationJob = createAsyncThunk('dataOperationJobApp/dataOperationJob/getDataOperationJob', async params => {
	// GetDataOperationJob
	const response = await axios.get('/api/Operation/JobById', {
		params: {
			Id: params.id,
		}
	});
	const data = await response.data;
	return data;
});


const dataOperationJobAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationJob, selectById: selectDataOperationJobById } = dataOperationJobAdapter.getSelectors(
	state => state.dataOperationJobApp.dataOperationJob
);

const dataOperationJobSlice = createSlice({
	name: 'dataOperationJobApp/dataOperationJob',
	initialState: dataOperationJobAdapter.getInitialState({
		dataOperationJob: {},
	}),
	reducers: {},
	extraReducers: {
		[getDataOperationJob.fulfilled]: (state, action) => {
			dataOperationJobAdapter.setAll(state, [action.payload.result.data]);
		}
	}
});
export default dataOperationJobSlice.reducer;
