import TableRow from '@material-ui/core/TableRow';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
	root: {
		height: 50,
		'& > *': {
			borderBottom: 'unset',
		},
		'&:nth-of-type(2n+1)': {
			backgroundColor: theme.palette.action.hover,
		},
		"&:hover": {
			backgroundColor: " rgba(0, 0, 0, 0.25) !important",
			'@media (hover: none)': {
			  backgroundColor: 'transparent',
			},
		}
	},
});

const StyledTableRow = withStyles(styles)(TableRow);
export default StyledTableRow;