
import { makeStyles } from '@material-ui/core/styles';

export const filterFormStyles = makeStyles(theme => ({
	root: {
		flexGrow: 1,
	},
	paper: {
		padding: theme.spacing(2),
		textAlign: 'center',
		color: theme.palette.text.secondary,
	},
	margin: {
		margin: theme.spacing(1)
	},
	extendedIcon: {
		marginRight: theme.spacing(1)
	},
	filterFormClass: {
		background: `linear-gradient(to left, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`,
		color: theme.palette.getContrastText(theme.palette.primary.main)
	},
	autocompleteStyle: {
		borderColor: 'red',
		color: 'red'
	},
	button: {
		margin: theme.spacing(1),
	},
}));
