import { UserManager, WebStorageStateStore } from 'oidc-client';
import React, { Component } from 'react';

var config = {
	response_mode: 'query',
	userStore: new WebStorageStateStore({ store: window.localStorage })
};
var mgr = new UserManager(config);

class OidcSlientRefresh extends Component {
	componentDidMount() {
		mgr.signinSilentCallback().catch(error => {
			console.log(error);
		});
	}

	render() {
		return <div>Loading ...</div>;
	}
}

export default OidcSlientRefresh;
