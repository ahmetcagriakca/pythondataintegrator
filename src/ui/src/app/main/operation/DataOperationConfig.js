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
			path: '/job/executions',
			component: React.lazy(() => import('./executions/DataOperationJobExecutions'))
		}
	]
};

export default DataOperationConfig;
