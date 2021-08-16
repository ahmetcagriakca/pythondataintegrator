import oidcService from 'app/services/oidcService';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from '@reduxjs/toolkit';
import { hideMessage, showMessage } from 'app/store/fuse/messageSlice';
import { setUserData, logoutUser } from './store/userSlice';

class Auth extends Component {
	state = {
		waitAuthCheck: true
	};

	async componentDidMount() {
		await oidcService.init();
		await oidcService.handleAuthentication();
		if(await oidcService.isAuthenticated()){
			const data = oidcService.getCurrentUser();
			this.props.setUserData(data);
		}

		// this.setState({ waitAuthCheck: false });
	}

	render() {
		return  <>{this.props.children}</>;
	}
}

function mapDispatchToProps(dispatch) {
	return bindActionCreators(
		{
			logout: logoutUser,
			setUserData,
			showMessage,
			hideMessage
		},
		dispatch
	);
}

export default connect(null, mapDispatchToProps)(Auth);
