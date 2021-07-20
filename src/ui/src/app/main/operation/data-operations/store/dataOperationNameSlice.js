import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getDataOperationName = createAsyncThunk('dataOperationsApp/dataOperationName/getDataOperationName', async params => {
	// GetDataOperation
	const response = await axios.get('/api/Lookup/DataOperation', {
	});
	const data = await response.data;
	return data.result.data;
});

export const dataOperationNameAdapter = createEntityAdapter({});

export const { selectAll: selectDataOperationName, selectById: selectDataOperationNameById } = dataOperationNameAdapter.getSelectors(
	state => state.dataOperationsApp.dataOperationName
);

const dataOperationNameSlice = createSlice({
	name: 'dataOperationsApp/dataOperationName',
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
