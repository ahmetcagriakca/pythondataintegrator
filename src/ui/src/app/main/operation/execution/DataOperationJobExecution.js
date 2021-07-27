import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationJobExecutionContent from './DataOperationJobExecutionContent';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function DataOperationJobExecution(props) {
	const icon = 'microwave';
	const title = 'DataOperationJobExecutions';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<DataOperationJobExecutionContent />
		</div>
	);
}

export default withReducer('dataOperationJobExecutionApp', reducer)(DataOperationJobExecution);
