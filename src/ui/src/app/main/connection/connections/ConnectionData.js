import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import TableContainer from '@material-ui/core/TableContainer';
import TablePagination from '@material-ui/core/TablePagination';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import React, { useEffect } from 'react';
import clsx from 'clsx';
import { useDispatch, useSelector } from 'react-redux';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import { withRouter, useParams } from 'react-router-dom';
import IconButton from '@material-ui/core/IconButton';
import Pagination from '@material-ui/lab/Pagination';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import Grid from '@material-ui/core/Grid';
import Icon from '@material-ui/core/Icon';
import { getConnections, selectConnections } from './store/connectionSlice';

const useStyles = makeStyles(themex => ({
	root: {
		flexGrow: 1
	},
	header: {
		background: `linear-gradient(to left, ${themex.palette.primary.dark} 0%, ${themex.palette.primary.main} 100%)`,
		color: themex.palette.getContrastText(themex.palette.primary.main)
	},
	headerIcon: {
		position: 'absolute',
		top: -64,
		left: 0,
		opacity: 0.04,
		fontSize: 512,
		width: 512,
		height: 512,
		pointerEvents: 'none'
	},
	table: {
		minWidth: 650
	},
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
}));

// table row
const StyledTableRow = withStyles(theme => ({
	root: {
		height: 57
	}
}))(TableRow);

const StyledTableCell = withStyles(theme => ({
	root: {
		padding: '0px 16px'
	}
}))(TableCell);

function descendingComparator(a, b, orderBy) {
	if (b[orderBy] < a[orderBy]) {
		return -1;
	}
	if (b[orderBy] > a[orderBy]) {
		return 1;
	}
	return 0;
}

function getComparator(order, orderBy) {
	return order === 'desc'
		? (a, b) => descendingComparator(a, b, orderBy)
		: (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort(array, comparator) {
	const stabilizedThis = array.map((el, index) => [el, index]);

	stabilizedThis.sort((a, b) => {
		const order = comparator(a[0], b[0]);
		if (order !== 0) return order;
		return a[1] - b[1];
	});
	return stabilizedThis.map(el => el[0]);
}

const headCells = [
	{ id: 'id', serviceName: 'id', numeric: false, disablePadding: false, label: 'Id' },
	{ id: 'name', serviceName: 'name', numeric: false, disablePadding: false, label: 'Name' },
	{ id: 'connectionType', serviceName: 'connectionType', numeric: false, disablePadding: false, label: 'Connection Type' },
];
function EnhancedTableHead(props) {
	const classes = useStyles();

	const { order, orderBy, onRequestSort } = props;
	const createSortHandler = property => event => {
		onRequestSort(event, property);
	};

	return (
		<TableHead>
			<TableRow className={classes.tableRowHeader}>
				{headCells.map(headCell => (
					<TableCell
						key={headCell.id}
						align={headCell.numeric ? 'right' : 'left'}
						padding={headCell.disablePadding ? 'none' : 'default'}
						sortDirection={orderBy === headCell.id ? order : false}
						className={classes.tableCell}
					>
						<TableSortLabel
							active={orderBy === headCell.id}
							direction={orderBy === headCell.id ? order : 'asc'}
							onClick={createSortHandler(headCell.id)}
						>
							{headCell.label}
						</TableSortLabel>
					</TableCell>
				))}
			</TableRow>
		</TableHead>
	);
}
function ConnectionData() {
	const dispatch = useDispatch();
	const classes = useStyles();
	const [order, setOrder] = React.useState('asc');
	const [orderBy, setOrderBy] = React.useState('id');
	const [selected, setSelected] = React.useState([]);
	const [page, setPage] = React.useState(0);
	const [rowsPerPage, setRowsPerPage] = React.useState(10);
	const connectionList = useSelector(selectConnections);

	const totalCount = useSelector(({ connectionApp }) => connectionApp.connection.count);
	const PageNumber = useSelector(({ connectionApp }) => connectionApp.connection.pageNumber);
	const PageSize = useSelector(({ connectionApp }) => connectionApp.connection.pageSize);

	const routeParams = useParams();
	routeParams.PageNumber = 0;
	routeParams.PageSize = PageSize === 0 ? 10 : PageSize;

	useEffect(() => {
		dispatchConnections(routeParams);;
	}, [dispatch]);

	const handleRequestSort = (event, orderByValue) => {
		const isAsc = orderBy === orderByValue && order === 'asc';
		setOrder(isAsc ? 'desc' : 'asc');
		console.log(order);
		setOrderBy(orderByValue);

		routeParams.OrderBy = orderByValue;
		routeParams.Order = order;
		dispatchConnections(routeParams);
	};
	const dispatchConnections = (routeParams)=>{
		let entities=getConnections(routeParams);;
		dispatch(entities);
	}
	const handleClick = (event, connectionName) => {
		const message = connectionName;
		alert(message);
	};

	const handleChangePage = (event, newPage) => {
		// const isNextPage = event.currentTarget.ariaLabel === 'Next page';
		// if (isNextPage && newPage === 1) {
		// 	newPage = 2;
		// }
		routeParams.PageSize = rowsPerPage;
		routeParams.PageNumber = newPage;
		dispatchConnections(routeParams);;
		setPage(newPage);
	};

	const handleChangeRowsPerPage = event => {
		routeParams.PageSize = event.target.value;
		routeParams.PageNumber = page;

		dispatchConnections(routeParams);;
		setRowsPerPage(event.target.value);
	};
	const isSelected = name => selected.indexOf(name) !== -1;

	return (
		<div
			className={clsx('flex flex-col flex-1 max-w-2x2 w-full mx-auto px-8 sm:px-32')}
			style={{ padding: '15px 40px 15px 40px' }}
		>
			<Paper style={{ borderTopLeftRadius: 30 }} className={classes.paper}>
				<TableContainer className={classes.container} style={{ maxHeight: 650, borderTopLeftRadius: 30 }}>
					<Table stickyHeader aria-label="sticky table" size="small">
						<EnhancedTableHead order={order} orderBy={orderBy} onRequestSort={handleRequestSort} />
						<TableBody>
							{stableSort(connectionList, getComparator(order, orderBy)).map((connection, index) => {
								const isItemSelected = isSelected(connection.Id);
								return (
									<StyledTableRow
										// className={classes.tableRow}

										hover
										aria-checked={isItemSelected}
										tabIndex={-1}
										key={connection.Id}
										selected={isItemSelected}
										onDoubleClick={event => handleClick(event, connection.Name)}
									>
										<TableCell align="left">{connection.Id}</TableCell>
										<TableCell align="left">{connection.Name}</TableCell>
										<TableCell align="left">{connection.ConnectionType.Name}</TableCell>
									</StyledTableRow>
								);
							})}
						</TableBody>
					</Table>
				</TableContainer>
				<TablePagination
					rowsPerPageOptions={[5, 10, 25, 50]}
					component="div"
					count={totalCount}
					rowsPerPage={rowsPerPage}
					page={page}
					onChangePage={handleChangePage}
					onChangeRowsPerPage={handleChangeRowsPerPage}
					style={{ fontSize: 'small' }}
				/>
			</Paper>
		</div>
	);
}
export default withRouter(ConnectionData);
