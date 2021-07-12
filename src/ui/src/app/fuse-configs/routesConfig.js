import React from 'react';
import { Redirect } from 'react-router-dom';
import FuseUtils from '@fuse/utils';
import appsConfigs from 'app/main/apps/appsConfigs';
import ConnectionConfig from 'app/main/connection/ConnectionConfig';
import DataOperationConfig from 'app/main/operation/DataOperationConfig';
import LoginConfig from 'app/main/login/LoginConfig';
import LogoutConfig from 'app/main/logout/LogoutConfig';
import pagesConfigs from 'app/main/pages/pagesConfigs';

const routeConfigs = [
	...appsConfigs,
	...pagesConfigs,
	ConnectionConfig,
	DataOperationConfig,
	LoginConfig,
	LogoutConfig,
];

const routes = [
	...FuseUtils.generateRoutesFromConfigs(routeConfigs, null),
	{
		path: '/',
		exact: true,
		component: () => <Redirect to="/apps/dashboards/project" />
	},
	{
		component: () => <Redirect to="/pages/errors/error-404" />
	}
];

export default routes;
