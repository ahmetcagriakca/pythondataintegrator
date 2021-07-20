import React from 'react';

const DataOperationConfig = {
	settings: {
		layout: {
			config: {}
		}
	},
	routes: [
		{
			path: '/dataoperations',
			component: React.lazy(() => import('./data-operations/DataOperations'))
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
