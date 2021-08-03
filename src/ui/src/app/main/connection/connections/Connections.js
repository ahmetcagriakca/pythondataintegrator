import React from 'react';
import withReducer from 'app/store/withReducer';

import ConnectionsData from './ConnectionsData';
import ConnectionsFilterForm from './ConnectionsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';
import { makeStyles } from '@material-ui/core/styles';
import Icon from '@material-ui/core/Icon';
import Fab from '@material-ui/core/Fab';
import Box from '@material-ui/core/Box';
import { useHistory } from 'react-router-dom';
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

function Connections() {
	const icon = 'microwave';
	const title = 'Connections';
	const classes = useStyles();
	const history = useHistory();
	function GotoComponent(path) {
		history.push('/'.concat(path));
	}
	const handleClick = (event, row) => {
		GotoComponent('connection')
	};
	return (
		<div style={{ position: 'relative' }}>
			<CommonHeader icon={icon} title={title} />
			<Box>

				<div className={classes.root}
					style={{ padding: '5px 40px 15px 40px' }}
				>
					<div className="flex flex-col flex-shrink-0 sm:flex-row items-center justify-between py-10"></div>
					<ConnectionsFilterForm />
				</div>
				<div
					className={clsx('flex flex-col flex-1 max-w-2x2 w-full mx-auto px-8 sm:px-32')}
				>
					<ConnectionsData />
					<div
						style={{ padding: '0 0 0 5px' }}
					>
						<Fab aria-label={"Add"} className={classes.fab} color={"primary"}
							onClick={handleClick}>
							<Icon>add</Icon>
						</Fab>
					</div>
				</div>
			</Box>
		</div>
	);
}

export default withReducer('connectionsApp', reducer)(Connections);
