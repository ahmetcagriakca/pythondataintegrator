import React from 'react';

const ConnectionConfig = {
	settings: {
		layout: {
			config: {}
		}
	},
	routes: [
		{
			path: '/connections',
			component: React.lazy(() => import('./connections/Connections'))
		}
	]
};

export default ConnectionConfig;
