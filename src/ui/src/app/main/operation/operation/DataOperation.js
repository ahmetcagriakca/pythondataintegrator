import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationContent from './DataOperationContent';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function DataOperation() {
	const icon = 'microwave';
	const title = 'DataOperation';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<DataOperationContent />
		</div>
	);
}

export default withReducer('dataOperationApp', reducer)(DataOperation);
