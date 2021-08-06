import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';

export const getWidgets = createAsyncThunk('analyticsDashboardApp/widgets/getWidgets', async () => {
	const response = await axios.get('/api/Dashboard');
	const data = await response.data;

	return data;
});

const widgetsAdapter = createEntityAdapter({});

export const { selectEntities: selectWidgetsEntities, selectById: selectWidgetById } = widgetsAdapter.getSelectors(
	state => state.analyticsDashboardApp.widgets
);

const widgetsSlice = createSlice({
	name: 'analyticsDashboardApp/widgets',
	initialState: widgetsAdapter.getInitialState({
		data: {},
	}),
	reducers: {},
	extraReducers: {
		// [getWidgets.fulfilled]: widgetsAdapter.setAll
		[getWidgets.fulfilled]: (state, action) => {
			widgetsAdapter.setAll(state, action.payload.result);
			state.data = action.payload.result;
		},
	}
});

export default widgetsSlice.reducer;
