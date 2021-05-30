import { authRoles } from 'app/auth';
import Login from './Login';
import OidcLoginRedirect from './tabs/oidc-login-redirect';
import OidcSlientRefresh from './tabs/oidc-slient-refresh';
const LoginConfig = {
	settings: {
		layout: {
			config: {
				navbar: {
					display: false
				},
				toolbar: {
					display: false
				},
				footer: {
					display: false
				},
				leftSidePanel: {
					display: false
				},
				rightSidePanel: {
					display: false
				}
			}
		}
	},
	auth: authRoles.onlyGuest,
	routes: [
		{
			path: '/login',
			component: Login
		},
		{
			path: '/oidc-login-redirect',
			component: OidcLoginRedirect
		},
		{
			path: '/oidc-slient-refresh',
			component: OidcSlientRefresh
		}
	]
};

export default LoginConfig;
