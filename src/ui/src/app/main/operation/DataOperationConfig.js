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
		}
	]
};

export default DataOperationConfig;
