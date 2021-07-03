import OidcService from 'app/services/oidcService';
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { setUserData } from 'app/auth/store/userSlice';
import { showMessage } from 'app/store/fuse/messageSlice';

function OidcLogin() {
	const dispatch = useDispatch();
	useEffect(() => {
		OidcService.login();
		OidcService.isAuthenticated(() => {
			dispatch(showMessage({ message: 'Logging in with OpenId Service' }));
			OidcService.getCurrentUser().then(data => {
				dispatch(setUserData(data));
				dispatch(showMessage({ message: 'Logged in with Auth0' }));
			});
		});
	}, [dispatch]);

	return null;
}

export default OidcLogin;
