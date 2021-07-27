import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationJobsData from './DataOperationJobsData';
import DataOperationJobsFilterForm from './DataOperationJobsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function DataOperationJobs(props) {
	const icon = 'microwave';
	const title = 'DataOperationJobs';


	const hasHeader = () => (props.HasHeader === undefined || props.HasHeader === null || props.HasHeader === true)

	return (
		<div style={{ position: 'relative' }}>
			{
				hasHeader() ? (
					<CommonHeader icon={icon} title={title} />
				) : ("")
			}

			<DataOperationJobsFilterForm DataOperationId={props.DataOperationId} />
			<DataOperationJobsData DataOperationId={props.DataOperationId} />
		</div>
	);
}

export default withReducer('dataOperationJobsApp', reducer)(DataOperationJobs);
