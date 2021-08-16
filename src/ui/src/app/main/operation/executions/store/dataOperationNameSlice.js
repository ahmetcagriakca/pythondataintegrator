import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getDataOperationName = createAsyncThunk('dataOperationJobExecutionsApp/dataOperationName/getDataOperationName', async (params, extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Lookup/DataOperation', {
		});
		const data = await response.data;
		return data.result.data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
});

export const dataOperationNameAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationName, selectById: selectDataOperationNameById } = dataOperationNameAdapter.getSelectors(
	state => state.dataOperationJobExecutionsApp.dataOperationName
);

const dataOperationNameSlice = createSlice({
	name: 'dataOperationJobExecutionsApp/dataOperationName',
	initialState: dataOperationNameAdapter.getInitialState({}),
	reducers: {

	},

	extraReducers: {
		[getDataOperationName.fulfilled]: (state, action) => {
			dataOperationNameAdapter.setAll(state, action.payload);
		}
	}
});

export default dataOperationNameSlice.reducer;
