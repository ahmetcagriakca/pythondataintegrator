import React from 'react';
import withReducer from 'app/store/withReducer';

import ConnectionsData from './ConnectionsData';
import ConnectionsFilterForm from './ConnectionsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function Connections() {
	const icon = 'microwave';
	const title = 'Connections';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<ConnectionsFilterForm />

			<ConnectionsData />
		</div>
	);
}

export default withReducer('connectionsApp', reducer)(Connections);
