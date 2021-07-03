import React from 'react';
import withReducer from 'app/store/withReducer';

import EnhancedTable from './SortingExample';
import reducer from './store';

function Sorting() {
	const icon = 'microwave';
	const title = 'Sorting';
	return (
		<div style={{ position: 'relative' }}>
			{/* <CommonHeader icon={icon} title={title} /> */}


			<EnhancedTable />
		</div>
	);
}

export default withReducer('sortingApp', reducer)(Sorting);