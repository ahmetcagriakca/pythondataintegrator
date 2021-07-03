import React from 'react';

const SortingConfig = {
	settings: {
		layout: {
			config: {}
		}
	},
	routes: [
		{
			path: '/sorting',
			component: React.lazy(() => import('./Sorting'))
		}
	]
};

export default SortingConfig;
