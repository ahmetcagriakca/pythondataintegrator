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
		},
		{
			path: '/connection/:id',
			component: React.lazy(() => import('./connection/Connection'))
		},
		{
			path: '/connection',
			component: React.lazy(() => import('./connection/Connection'))
		}
	]
};

export default ConnectionConfig;
