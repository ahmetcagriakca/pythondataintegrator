import { createSlice } from '@reduxjs/toolkit';
export const SET_SNACKBAR = 'teamly/settings/SET_SNACKBAR';

const initialState = {
	snackbarOpen: false,
	snackbarType: 'success',
	snackbarMessage: ''
};

export const setSnackbar = (snackbarOpen, snackbarType = 'success', snackbarMessage = '') => ({
	type: SET_SNACKBAR,
	snackbarOpen,
	snackbarType,
	snackbarMessage
});

const snackbarSlice = createSlice({
	name: 'snackbarsApp/snackbars',
	initialState,
	reducers: {
		setSnackbar: (state = initialState, action) => {
			switch (action.type) {
				case SET_SNACKBAR:
					// const {  } = action;
					return {
						...state,
						snackbarOpen,
						snackbarType,
						snackbarMessage
					};
				default:
					return state;
			}
		}
	},
	extraReducers: {}
});

export const { snackbarOpen, snackbarMessage, snackbarType } = snackbarSlice.actions;

export default snackbarSlice.reducer;
