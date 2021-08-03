import TableCell from '@material-ui/core/TableCell';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
	head: {
		color: theme.palette.common.white,
	},
	body: {
		fontSize: 14,
	}
});

const StyledTableCell = withStyles(styles)(TableCell);
export default  StyledTableCell;