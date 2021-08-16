import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';


export const getOperationJob = createAsyncThunk('dataOperationJobApp/dataOperationJob/getDataOperationJob', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Operation/JobById', {
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

export const postScheduleCronJob = createAsyncThunk('dataOperationJobApp/dataOperationJob/postScheduleCronJob', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Schedule/CronJob', params);
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});
export const postScheduleJob = createAsyncThunk('dataOperationJobApp/dataOperationJob/postScheduleJob', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.post('/api/Schedule/Job', params);
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const deleteScheduleCronJob = createAsyncThunk('dataOperationJobApp/dataOperationJob/deleteScheduleCronJob', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.delete('/api/Schedule/CronJob', {
			data: params
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const deleteScheduleJob = createAsyncThunk('dataOperationJobApp/dataOperationJob/deleteScheduleJob', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.delete('/api/Schedule/Job', {
			data: params
		});
		const data = await response.data;
		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const clearDataOperationJob = createAsyncThunk('dataOperationJobApp/dataOperationJob/clearOperation', async params => {
	return {};
});

const dataOperationJobAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationJob, selectById: selectDataOperationJobById } = dataOperationJobAdapter.getSelectors(
	state => state.dataOperationJobApp.dataOperationJob
);

const dataOperationJobSlice = createSlice({
	name: 'dataOperationJobApp/dataOperationJob',
	initialState: dataOperationJobAdapter.getInitialState({
		data: {},
	}),
	reducers: {},
	extraReducers: {
		[getOperationJob.fulfilled]: (state, action) => {
			dataOperationJobAdapter.setAll(state, [action.payload.result.data]);
			state.data = action.payload.result.data;
		},
		[clearDataOperationJob.fulfilled]: (state, action) => {
			dataOperationJobAdapter.setAll(state, []);
			state.data = {};
		},
	}
});
export default dataOperationJobSlice.reducer;
