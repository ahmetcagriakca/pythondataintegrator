import React from 'react';
import withReducer from 'app/store/withReducer';

import ConnectionsData from './ConnectionsData';
import ConnectionsFilterForm from './ConnectionsFilterForm';
import CommonHeader from '../../common/CommonHeader';
import reducer from './store';
import { makeStyles, createStyles } from '@material-ui/core/styles';
import Icon from '@material-ui/core/Icon';
import Fab from '@material-ui/core/Fab';
import Box from '@material-ui/core/Box';
import { useHistory } from 'react-router-dom';

const useStyles = makeStyles((theme) =>

	createStyles({
		fab: {
			// position: 'absolute',
			// bottom: theme.spacing(2),
			// right: theme.spacing(2),
			margin: 0,
			top: 'auto',
			right: 40,
			bottom: 40,
			left: 'auto',
			position: 'fixed',
		}
	}),
);

function Connections() {
	const classes = useStyles();
	const history = useHistory();
	const icon = 'microwave';
	const title = 'Connections';
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
				<ConnectionsFilterForm />

				<ConnectionsData />
			</Box>

			<Fab aria-label={"Add"} className={classes.fab} color={"primary"}
				onClick={handleClick}>
				<Icon>add</Icon>
			</Fab>
		</div>
	);
}

export default withReducer('connectionsApp', reducer)(Connections);
