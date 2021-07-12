import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationsData from './DataOperationsData';
import DataOperationsFilterForm from './DataOperationsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';

function DataOperations() {
	const icon = 'microwave';
	const title = 'DataOperations';
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<DataOperationsFilterForm />

			<DataOperationsData />
		</div>
	);
}

export default withReducer('dataOperationsApp', reducer)(DataOperations);
