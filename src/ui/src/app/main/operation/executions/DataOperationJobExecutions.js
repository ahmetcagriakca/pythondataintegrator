import React from 'react';
import withReducer from 'app/store/withReducer';

import DataOperationJobExecutionsData from './DataOperationJobExecutionsData';
import DataOperationJobExecutionsFilterForm from './DataOperationJobExecutionsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';
import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';

const useStyles = makeStyles((theme) => ({
	root: {
		flexGrow: 1,
	},
	fab: {
		// position: 'absolute',
		// bottom: theme.spacing(2),
		// right: theme.spacing(2),
		margin: 0,
		top: 'auto',
		right: 'auto',
		bottom: 12,
		left: 'auto',
		position: 'fixed',
	}
}));

function DataOperationJobExecutions(props) {
	const icon = 'microwave';
	const title = 'DataOperationJobExecutions';
	const classes = useStyles();
	const hasHeader = () => (props.HasHeader === undefined || props.HasHeader === null || props.HasHeader === true)
	return (
		<div style={{ position: 'relative' }}>
			{
				hasHeader() ? (
					<CommonHeader icon={icon} title={title} />
				) : ("")
			}
			<div className={classes.root}
				style={{ padding: '15px 40px 15px 40px' }}
			>
				<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>
				<DataOperationJobExecutionsFilterForm DataOperationId={props.DataOperationId} />

			</div>
			<div
				className={clsx('flex flex-col flex-1 max-w-2x2 w-full mx-auto px-8 sm:px-32')}
			>
				<DataOperationJobExecutionsData DataOperationId={props.DataOperationId} />
			</div>
		</div>
	);
}

export default withReducer('dataOperationJobExecutionsApp', reducer)(DataOperationJobExecutions);
