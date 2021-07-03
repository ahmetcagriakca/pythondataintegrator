const OIDC_CONFIG = {
	authority: window.AUTHORITY,
	client_id: window.CLIENT_ID,
	redirect_uri: window.REDIRECT_URI,
	scope: 'openid profile Pdi.Api',
	response_type: 'code',
	post_logout_redirect_uri: window.POST_REDIRECT_URI,
	slient_redirect_uri: window.SLIENT_REDIRECT_URI
};

export default OIDC_CONFIG;
