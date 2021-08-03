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
	},
});

const StyledTableRow = withStyles(styles)(TableRow);
export default  StyledTableRow;