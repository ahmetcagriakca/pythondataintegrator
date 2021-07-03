import { UserManager, WebStorageStateStore } from 'oidc-client';
import React, { Component } from 'react';

var config = {
	response_mode: 'query',
	userStore: new WebStorageStateStore({ store: window.localStorage })
};
var mgr = new UserManager(config);

class OidcLoginRedirect extends Component {
	componentDidMount() {
		mgr.signinRedirectCallback().then(
			function (user) {
				window.history.replaceState({}, window.document.title, window.location.origin);
				let returnUrl = localStorage.getItem('returnUrl');
				if (returnUrl) {
					localStorage.removeItem('returnUrl');
				} else {
					returnUrl = '/';
				}
				
				window.location.href = '/';
			},
			error => {
				console.error(error);
			}
		);
	}

	render() {
		return <div>Loading ...</div>;
	}
}

export default OidcLoginRedirect;
