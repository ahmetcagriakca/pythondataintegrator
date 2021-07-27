import React from 'react';

const DataOperationConfig = {
	settings: {
		layout: {
			config: {}
		}
	},
	routes: [
		{
			path: '/operations',
			component: React.lazy(() => import('./operations/DataOperations'))
		},
		{
			path: '/operation/:id',
			component: React.lazy(() => import('./operation/DataOperation'))
		},
		{
			path: '/jobs',
			component: React.lazy(() => import('./jobs/DataOperationJobs'))
		},
		{
			path: '/operationjob/:id',
			component: React.lazy(() => import('./job/DataOperationJob'))
		},
		{
			path: '/job/executions',
			component: React.lazy(() => import('./executions/DataOperationJobExecutions'))
		},
		{
			path: '/operationjobexecution/:id',
			component: React.lazy(() => import('./execution/DataOperationJobExecution'))
		},
	]
};

export default DataOperationConfig;
