import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import clsx from 'clsx';
import { useDispatch, useSelector } from 'react-redux';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import { withRouter, useParams } from 'react-router-dom';
import { getDataOperations, selectDataOperations } from './store/dataOperationsSlice';
import CustomPagination from '../../common/components/CustomPagination';
import EnhancedTableHead from '../../common/components/EnhancedTableHead';


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

function stableSort(source, comparator) {
	const stabilizedThis = source.map((el, index) => [el, index]);

	stabilizedThis.sort((a, b) => {
		const order = comparator(a[0], b[0]);
		if (order !== 0) return order;
		return a[1] - b[1];
	});
	return stabilizedThis.map(el => el[0]);
}

const headCells = [
	{ id: 'id', orderBy: 'DataOperation.Id', numeric: true, disablePadding: true, label: 'Id' },
	{ id: 'name', orderBy: 'DataOperation.Name', numeric: false, disablePadding: true, label: 'Name' },
	{ id: 'contacts', orderBy: null, numeric: false, disablePadding: true, sortable: false,label: 'Contacts' },
	{ id: 'definitionId', orderBy: 'Definition.Id', numeric: false, disablePadding: true, label: 'Definition Id' },
	{ id: 'creationDate', orderBy: 'DataOperation.CreationDate', numeric: false, disablePadding: true, label: 'Creation Date' },
	{ id: 'lastUpdatedDate', orderBy: 'DataOperation.LastUpdatedDate', numeric: false, disablePadding: true, label: 'Last Updated Date' },
];
function DataOperationsData() {
	const dispatch = useDispatch();
	const classes = useStyles();
	const [order, setOrder] = React.useState('asc');
	const [orderBy, setOrderBy] = React.useState('DataOperation.Id');
	const [selected] = React.useState([]);
	const [page, setPage] = React.useState(1);
	const [rowsPerPage, setRowsPerPage] = React.useState(10);
	const dataOperationsList = useSelector(selectDataOperations);

	const totalCount = useSelector(({ dataOperationsApp }) => dataOperationsApp.dataOperations.count);
	const PageNumber = useSelector(({ dataOperationsApp }) => {
		if (page !== dataOperationsApp.dataOperations.pageNumber) {
			setPage(dataOperationsApp.dataOperations.pageNumber)
		}
		return dataOperationsApp.dataOperations.pageNumber
	});
	const PageSize = useSelector(({ dataOperationsApp }) => dataOperationsApp.dataOperations.pageSize);

	const routeParams = useParams();
	routeParams.PageNumber = PageNumber;
	routeParams.PageSize = PageSize === 0 ? 10 : PageSize;
	routeParams.OrderBy = orderBy;
	routeParams.Order = order;

	useEffect(() => {
		dispatch(getDataOperations(routeParams));
	}, [dispatch,routeParams]);

	const handleRequestSort = (event, orderByValue) => {
		const isAsc = orderBy === orderByValue && order === 'asc';
		let orderValue = isAsc ? 'desc' : 'asc'
		setOrder(orderValue);
		console.log(order);
		setOrderBy(orderByValue);
		routeParams.PageSize = rowsPerPage;
		routeParams.PageNumber = page;
		routeParams.OrderBy = orderByValue;
		routeParams.Order = orderValue;
		dispatch(getDataOperations(routeParams));
	};

	const handleClick = (event, dataOperationName) => {
		const message = dataOperationName.concat(' isimli dataOperation git');
		alert(message);
	};

	const handleChangePage = (event, newPage) => {
		routeParams.PageSize = rowsPerPage;
		routeParams.PageNumber = newPage;
		dispatch(getDataOperations(routeParams));
		setPage(newPage);
	};

	const handleChangeRowsPerPage = event => {
		routeParams.PageSize = event.target.value;
		routeParams.PageNumber = page;

		dispatch(getDataOperations(routeParams));
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
						<EnhancedTableHead order={order} orderBy={orderBy} onRequestSort={handleRequestSort} headCells={headCells}/>
						<TableBody>
							{stableSort(dataOperationsList, getComparator(order, orderBy)).map((dataOperation, index) => {
								const isItemSelected = isSelected(dataOperation.id);
								return (
									<StyledTableRow
										hover
										aria-checked={isItemSelected}
										tabIndex={-1}
										key={dataOperation.id}
										selected={isItemSelected}
										onDoubleClick={event => handleClick(event, dataOperation.name)}
									>
										
										<TableCell align="left">{dataOperation.id}</TableCell>
										<TableCell align="left">{dataOperation.name}</TableCell>
										<TableCell align="left">
											{
												dataOperation.contacts!==null?(
													<Table size="small" >
														<TableBody>
															{dataOperation.contacts.map((contactRow) => (
																<TableRow key={contactRow.id}>
																	<TableCell>{contactRow.email}</TableCell>
																</TableRow>
															))}
														</TableBody>
													</Table>
												):
												("")
											}
										</TableCell>
										<TableCell align="left">{dataOperation.definitionId}</TableCell>
										<TableCell align="left">{dataOperation.creationDate}</TableCell>
										<TableCell align="left">{dataOperation.lastUpdatedDate}</TableCell>
									</StyledTableRow>
								);
							})}
						</TableBody>
					</Table>
				</TableContainer>
				<CustomPagination
					rowsPerPage={rowsPerPage}
					page={page}
					totalCount={totalCount}
					handleChangePage={handleChangePage}
					handleChangeRowsPerPage={handleChangeRowsPerPage}
				/>
			</Paper>
		</div>
	);
}

export default withRouter(DataOperationsData);
