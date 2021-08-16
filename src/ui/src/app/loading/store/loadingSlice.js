import { createSlice, createAsyncThunk, createEntityAdapter } from '@reduxjs/toolkit';

export const initialState = {
	loading: false,
	refCount: 0
};

export const setLoading = createAsyncThunk('app/loading/setLoading', async isLoading => {
	return {
		isLoading: isLoading
	};
});

// export const setLoading = (isLoading) => {
// 	if (isLoading) {
// 		initialState.refCount++;
// 		initialState.loading = true;
// 	} else if (initialState.refCount > 0) {
// 		initialState.refCount--;
// 		initialState.isLoading = (initialState.refCount > 0);
// 	}
// }

const loadingSlice = createSlice({
	name: 'app/loading',
	initialState,
	reducers: {
	},
	extraReducers: {
		[setLoading.fulfilled]: (state, action) => {
			if (action.payload.isLoading) {
				state.refCount++;
				state.loading = true;
			} else if (state.refCount > 0) {
				state.refCount--;
				state.loading = (state.refCount > 0);
			}
		},
	}
});

// export const { setLoading } = loadingSlice.actions;

export default loadingSlice.reducer;
