import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationJobExecutionsData from './DataOperationJobExecutionsData';
import DataOperationJobExecutionsFilterForm from './DataOperationJobExecutionsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function DataOperationJobExecutions(props) {
	const icon = 'microwave';
	const title = 'DataOperationJobExecutions';
	const hasHeader = () => (props.HasHeader === undefined || props.HasHeader === null || props.HasHeader === true)
	return (
		<div style={{ position: 'relative' }}>
			{
				hasHeader() ? (
					<CommonHeader icon={icon} title={title} />
				) : ("")
			}
			<DataOperationJobExecutionsFilterForm DataOperationId={props.DataOperationId} />

			<DataOperationJobExecutionsData DataOperationId={props.DataOperationId} />
		</div>
	);
}

export default withReducer('dataOperationJobExecutionsApp', reducer)(DataOperationJobExecutions);
