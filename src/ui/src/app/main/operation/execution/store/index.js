import { combineReducers } from '@reduxjs/toolkit';
import dataOperationJobExecution from './dataOperationJobExecutionSlice';
import dataOperationJobExecutionIntegrations from './dataOperationJobExecutionIntegrationsSlice';
import dataOperationJobExecutionLogs from './dataOperationJobExecutionLogsSlice';
import statusName from './statusNameSlice';

const reducer = combineReducers({
	dataOperationJobExecution,
	dataOperationJobExecutionIntegrations,
	dataOperationJobExecutionLogs,
	statusName,
});

export default reducer;
