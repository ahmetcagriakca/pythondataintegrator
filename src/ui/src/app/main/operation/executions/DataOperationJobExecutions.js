import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationJobExecutionsData from './DataOperationJobExecutionsData';
import DataOperationJobExecutionsFilterForm from './DataOperationJobExecutionsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function DataOperationJobExecutions() {
	const icon = 'microwave';
	const title = 'DataOperationJobExecutions';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<DataOperationJobExecutionsFilterForm />

			<DataOperationJobExecutionsData />
		</div>
	);
}

export default withReducer('dataOperationJobExecutionsApp', reducer)(DataOperationJobExecutions);
