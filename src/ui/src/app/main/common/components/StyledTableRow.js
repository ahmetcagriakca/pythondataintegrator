import TableRow from '@material-ui/core/TableRow';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
	root: {
		height: 50
	}
});

const StyledTableRow = withStyles(styles)(TableRow);
export default  StyledTableRow;