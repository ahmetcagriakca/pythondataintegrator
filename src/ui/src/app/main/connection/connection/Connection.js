import React from 'react';
import withReducer from 'app/store/withReducer';

import ConnectionContent from './ConnectionContent';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function Connection() {
	const icon = 'microwave';
	const title = 'Connection';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<ConnectionContent />
		</div>
	);
}

export default withReducer('connectionApp', reducer)(Connection);
