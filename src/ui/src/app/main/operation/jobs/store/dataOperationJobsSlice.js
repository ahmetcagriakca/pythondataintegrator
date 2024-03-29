import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';


export const getDataOperationJobs = createAsyncThunk('dataOperationJobsApp/dataOperationJobs/getDataOperationJobs', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Operation/Job', {
			params: {
				PageNumber: params.PageNumber,
				PageSize: params.PageSize,
				OrderBy: params.OrderBy,
				Order: params.Order,
				DataOperationId: params.DataOperationId,
				DataOperationName: params.DataOperationName,
				OnlyCron: params.OnlyCron,
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


const dataOperationJobsAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationJobs, selectById: selectDataOperationJobById } = dataOperationJobsAdapter.getSelectors(
	state => state.dataOperationJobsApp.dataOperationJobs
);

const dataOperationJobSlice = createSlice({
	name: 'dataOperationJobsApp/dataOperationJobs',
	initialState: dataOperationJobsAdapter.getInitialState({
		count: 0,
		dataOperationJob: {},
		pageNumber: 1,
		pageSize: 0
	}),
	reducers: {},
	extraReducers: {
		[getDataOperationJobs.fulfilled]: (state, action) => {
			dataOperationJobsAdapter.setAll(state, action.payload.result.data);
			state.pageNumber = action.payload.result.pageNumber;
			state.pageSize = action.payload.result.pageSize;
			state.count = action.payload.result.count;
		}
	}
});
export default dataOperationJobSlice.reducer;
