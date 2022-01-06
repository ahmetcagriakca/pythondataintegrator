import React from 'react';
import withReducer from 'app/store/withReducer';
import ConnectionSqlContent from './ConnectionSqlContent';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';
import { makeStyles } from '@material-ui/core/styles';

export const useStyles = makeStyles(theme => ({
	root: {
		flexGrow: 1,
	}
}));
function ConnectionSql() {
	const icon = 'https';
	const title = 'Connection';
	const classes = useStyles();
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />

			<div className={classes.root}
				style={{ padding: '15px 40px 15px 40px' }}
			>
				<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>

				<ConnectionSqlContent />
			</div>
		</div>
	);
}

export default withReducer('connectionSqlApp', reducer)(ConnectionSql);
