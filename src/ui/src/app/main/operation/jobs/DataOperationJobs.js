import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationJobsData from './DataOperationJobsData';
import DataOperationJobsFilterForm from './DataOperationJobsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function DataOperationJobs() {
	const icon = 'microwave';
	const title = 'DataOperationJobs';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<DataOperationJobsFilterForm />

			<DataOperationJobsData />
		</div>
	);
}

export default withReducer('dataOperationJobsApp', reducer)(DataOperationJobs);
