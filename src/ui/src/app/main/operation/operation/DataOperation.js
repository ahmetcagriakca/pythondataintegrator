import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationContent from './DataOperationContent';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
	root: {
		flexGrow: 1,
	},
}));
function DataOperation() {
	const icon = 'microwave';
	const title = 'DataOperation';
	const classes = useStyles();
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<div className={classes.root}
				style={{ padding: '15px 40px 15px 40px' }}
			>
				<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>

				<DataOperationContent />
			</div>
		</div>
	);
}

export default withReducer('dataOperationApp', reducer)(DataOperation);
