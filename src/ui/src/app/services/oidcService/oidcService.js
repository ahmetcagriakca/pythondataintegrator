import { UserManager, WebStorageStateStore } from 'oidc-client';
import OIDC_CONFIG from './oidcServiceConfig';
import jwtDecode from 'jwt-decode';

class OidcService {
	_userManager;
	_user;


	init() {
		if (Object.entries(OIDC_CONFIG).length === 0 && OIDC_CONFIG.constructor === Object) {
			if (process.env.NODE_ENV === 'development') {
				console.warn('Missing oidc configuration at src/app/services/oidc/oidcserviceconfig.js');
			}
			return;
		}

		this._userManager = new UserManager({
			authority: OIDC_CONFIG.authority,
			client_id: OIDC_CONFIG.client_id,
			redirect_uri: OIDC_CONFIG.redirect_uri,
			scope: OIDC_CONFIG.scope,
			response_type: OIDC_CONFIG.response_type,
			post_logout_redirect_uri: OIDC_CONFIG.post_logout_redirect_uri,
			userStore: new WebStorageStateStore({ store: window.localStorage }),
			response_mode: 'query',
			automaticSilentRenew: true,
			revokeAccessTokenOnSignout: true,
			silent_redirect_uri: OIDC_CONFIG.slient_redirect_uri
		});
	}

	handleAuthentication = () => {
		if (!this._userManager) {
			return false;
		}

		var promise = this._userManager.getUser().then(user => {
			if (user && !user.expired) {
				this._user = user;
			}
		});

		return promise;
	};

	login = () => {
		if (!this._userManager) {
			return false;
		}

		if (this._user != null) {
			return;
		}

		return this._userManager.signinRedirect();
	};

	logout = () => {
		this._userManager.signoutRedirect();
		this._user = null;
		this.UserManager.clearStaleState();
		this._userManager.removeUser();
	};

	isAuthenticated = () => {
		if (!this._userManager) {
			return false;
		}

		return this._user && this._user.access_token && !this._user.expired;
	};

	getAccessToken = () => {
		return this._user ? this._user.access_token : '';
	};

	signoutRedirectCallback = () => {
		return this._userManager.signoutRedirectCallback();
	};

	getCurrentUser = () => {
		const decoded = jwtDecode(this.getAccessToken());
		return {
			id: this._user.profile.sub,
			name: this._user.profile.name,
			roles: decoded.role
		};
	};
}

const instance = new OidcService();

export default instance;
