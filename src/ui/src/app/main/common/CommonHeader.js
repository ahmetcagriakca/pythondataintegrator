import { makeStyles } from '@material-ui/core/styles';
import FuseAnimate from '@fuse/core/FuseAnimate';
import Icon from '@material-ui/core/Icon';
import Typography from '@material-ui/core/Typography';
import clsx from 'clsx';
import React from 'react';

const useStyles = makeStyles(theme => ({
	header: {
		background: `linear-gradient(to left, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`,
		color: theme.palette.getContrastText(theme.palette.primary.main),
		borderTopLeftRadius: '25px',
		margin: '3px'
	},
	headerIcon: {
		position: 'absolute',
		top: -64,
		left: 0,
		opacity: 0.04,
		fontSize: 512,
		width: 256,
		height: 256,
		pointerEvents: 'none'
	},
	headerTitle: {
		fontSize: 25,
		fontWeight: 'bold'
	}
}));

function CommonHeader(props) {
	const classes = useStyles(props);
	const { icon, title } = props;
	return (
		<div className={clsx('sm:px-32', classes.header)}>
			<div className="flex flex-shrink items-center" style={{ padding: '15px 5px 15px 5px' }}>
				<div className="flex items-center">
					<FuseAnimate animation="transition.expandIn" delay={300}>
						<Icon className="text-32">{icon}</Icon>
					</FuseAnimate>
					<FuseAnimate animation="transition.slideLeftIn" delay={300}>
						<Typography className={classes.headerTitle}>{title}</Typography>
					</FuseAnimate>
				</div>
			</div>
		</div>
	);
}

export default CommonHeader;
