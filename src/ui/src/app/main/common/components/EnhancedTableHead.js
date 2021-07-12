import TableHead from '@material-ui/core/TableHead';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import { withStyles } from '@material-ui/core/styles';
import React from 'react';
import PropTypes from 'prop-types';

const styles = theme => ({
	tableRowHeader: {
		height: 70
	},
	tableCell: {
		padding: '0px 16px',
		// backgroundColor: 'gainsboro',
		backgroundColor: '#006565',
		color: 'white',
		// '&:hover': {
		// 	backgroundColor: 'blue !important'
		// }
		hover: {
			'&:hover': {
				backgroundColor: 'green !important'
			}
		}
	}
});
class EnhancedTableHead extends React.Component {
    static propTypes = {
        onRequestSort: PropTypes.func
    }
    createSortHandler = property => event => {
        
        if (
            typeof this.props.onRequestSort !== 'undefined' &&
            typeof this.props.onRequestSort === 'function'
        ) {
            this.props.onRequestSort(event, property);
        }
    };
    render() {

        const { 
            classes,
            order, 
            orderBy, 
            headCells , 
            
        } = this.props;

        return (
            <TableHead>
                <TableRow className={classes.tableRowHeader}>
                    {headCells.map(headCell => (
                        <TableCell
                            key={headCell.id}
                            align={headCell.numeric ? 'right' : 'left'}
                            padding={headCell.disablePadding ? 'none' : 'normal'}
                            sortDirection={orderBy === headCell.orderBy ? order : false}
                            className={classes.tableCell}
                        >
                            <TableSortLabel
                                active={orderBy === headCell.orderBy}
                                direction={orderBy === headCell.orderBy ? order : 'asc'}
                                onClick={this.createSortHandler(headCell.orderBy)}
                            >
                                {headCell.label}
                            </TableSortLabel>
                        </TableCell>
                    ))}
                </TableRow>
            </TableHead>
        );
    }
}

export default withStyles(styles)(EnhancedTableHead);