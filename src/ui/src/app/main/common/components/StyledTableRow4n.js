import TableRow from '@material-ui/core/TableRow';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
	root: {
		height: 50,
		'& > *': {
			borderBottom: 'unset',
		},
		'&:nth-of-type(4n+1)': {
			backgroundColor: theme.palette.action.hover,
		},
	},
});

const StyledTableRow4n = withStyles(styles)(TableRow);
export default  StyledTableRow4n;