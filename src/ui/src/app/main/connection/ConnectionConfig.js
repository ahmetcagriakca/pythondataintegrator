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
			path: '/connection/sql/:id',
			component: React.lazy(() => import('./connectionSql/ConnectionSql'))
		},
		{
			path: '/connection/sql',
			component: React.lazy(() => import('./connectionSql/ConnectionSql'))
		}
	]
};

export default ConnectionConfig;
