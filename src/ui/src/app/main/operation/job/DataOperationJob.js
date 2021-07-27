import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationJobContent from './DataOperationJobContent';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function DataOperationJob() {
	const icon = 'microwave';
	const title = 'DataOperationJob';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<DataOperationJobContent />
		</div>
	);
}

export default withReducer('dataOperationJobApp', reducer)(DataOperationJob);
