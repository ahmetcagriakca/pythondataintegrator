import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getStatusName = createAsyncThunk('dataOperationJobExecutionApp/statusName/getStatusName', async params => {
	const response = await axios.get('/api/Lookup/Status', {
	});
	const data = await response.data;
	return data.result.data;
});

export const statusNameAdapter = createEntityAdapter({});

export const { selectAll: selectStatusName, selectById: selectStatusNameById } = statusNameAdapter.getSelectors(
	state => state.dataOperationJobExecutionApp.statusName
);

const statusNameSlice = createSlice({
	name: 'dataOperationJobExecutionApp/statusName',
	initialState: statusNameAdapter.getInitialState({}),
	reducers: {

	},

	extraReducers: {
		[getStatusName.fulfilled]: (state, action) => {
			statusNameAdapter.setAll(state, action.payload);
		}
	}
});

export default statusNameSlice.reducer;
