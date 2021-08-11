import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';
import axios from './axios';
import { setLoading } from 'app/loading/store/loadingSlice';

export const getWidgets = createAsyncThunk('analyticsDashboardApp/widgets/getWidgets', async (params,extra) => {
	try {
		extra.dispatch(setLoading(true))
		const response = await axios.get('/api/Dashboard');
		const data = await response.data;

		return data;
	}
	finally {
		extra.dispatch(setLoading(false))
	}
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
			widgetsAdapter.setAll(state, action.payload.result.data);
			state.data = action.payload.result.data;
		},
	}
});

export default widgetsSlice.reducer;
