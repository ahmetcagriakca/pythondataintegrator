import React from 'react';
import withReducer from 'app/store/withReducer';

import ConnectionHeader from './ConnectionHeader';
import ConnectionData from './ConnectionData';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function Connection() {
	const icon = 'microwave';
	const title = 'Connections';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			{/* <ConnectionFilterForm /> */}

			<ConnectionData />
		</div>
	);
}

export default withReducer('connectionApp', reducer)(Connection);
