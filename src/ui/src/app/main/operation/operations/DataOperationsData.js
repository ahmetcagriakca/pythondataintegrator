import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import clsx from 'clsx';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import { getDataOperations, selectDataOperations } from './store/dataOperationsSlice';
import CustomPagination from '../../common/components/CustomPagination';
import EnhancedTableHead from '../../common/components/EnhancedTableHead';
import StyledTableRow from '../../common/components/StyledTableRow';
import { stableSort, getComparator } from '../../common/utils/TableUtils';
import { tableStyles } from '../../common/styles/TableStyles';
import { useHistory } from 'react-router-dom';


function DataOperationsData() {
	const dispatch = useDispatch();
	const classes = tableStyles();
	const history = useHistory();
	const headCells = [
		{ id: 'id', orderBy: 'DataOperation.Id', numeric: true, disablePadding: true, label: 'Id' },
		{ id: 'name', orderBy: 'DataOperation.Name', numeric: false, disablePadding: true, label: 'Name' },
		{ id: 'contacts', orderBy: null, numeric: false, disablePadding: true, sortable: false, label: 'Contacts' },
		{ id: 'definitionId', orderBy: 'Definition.Id', numeric: false, disablePadding: true, label: 'Definition Id' },
		{ id: 'creationDate', orderBy: 'DataOperation.CreationDate', numeric: false, disablePadding: true, label: 'Creation Date' },
		{ id: 'lastUpdatedDate', orderBy: 'DataOperation.LastUpdatedDate', numeric: false, disablePadding: true, label: 'Last Updated Date' },
		{ id: 'isDeleted', orderBy: 'DataOperation.IsDeleted', numeric: false, disablePadding: true, label: 'Is Deleted' },
	];
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
	}, [dispatch, routeParams]);

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

	function GotoComponent(path) {
		history.push('/'.concat(path));
	}
	const handleClick = (event, row) => {
		GotoComponent('operation/'+row.id)
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
						<EnhancedTableHead order={order} orderBy={orderBy} onRequestSort={handleRequestSort} headCells={headCells} />
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
										onDoubleClick={event => handleClick(event, dataOperation)}
									>

										<TableCell align="left">{dataOperation.id}</TableCell>
										<TableCell align="left">{dataOperation.name}</TableCell>
										<TableCell align="left">
											{
												dataOperation.contacts !== null ? (
													<Table size="small" >
														<TableBody>
															{dataOperation.contacts.map((contactRow) => (
																<TableRow key={contactRow.id}>
																	<TableCell>{contactRow.email}</TableCell>
																</TableRow>
															))}
														</TableBody>
													</Table>
												) :
													("")
											}
										</TableCell>
										<TableCell align="left">{dataOperation.definitionId}</TableCell>
										<TableCell align="left">{dataOperation.creationDate}</TableCell>
										<TableCell align="left">{dataOperation.lastUpdatedDate}</TableCell>
										<TableCell align="left">{dataOperation.isDeleted}</TableCell>
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
