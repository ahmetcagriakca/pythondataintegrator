import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import Paper from '@material-ui/core/Paper';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import clsx from 'clsx';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import { getDataOperationJobExecutions, selectDataOperationJobExecutions } from './store/dataOperationJobExecutionsSlice';
import CustomPagination from '../../common/components/CustomPagination';
import EnhancedTableHead from '../../common/components/EnhancedTableHead';
import StyledTableRow from '../../common/components/StyledTableRow';
import { stableSort, getComparator } from '../../common/utils/TableUtils';
import { tableStyles } from '../../common/styles/TableStyles';

function DataOperationJobExecutionsData() {
	const dispatch = useDispatch();
	const classes = tableStyles();
	const headCells = [
		{ id: 'id', orderBy: 'DataOperationJobExecution.Id', numeric: true, disablePadding: true, label: 'Id' },
		{ id: 'jobId', orderBy: 'DataOperationJob.Id', numeric: true, disablePadding: true, label: 'Job Id' },
		{ id: 'dataOperationName', orderBy: 'DataOperation.Name', numeric: false, disablePadding: true, label: 'Name' },
		{ id: 'scheduleInfo', orderBy: null, numeric: false, disablePadding: true, label: 'Schedule Info' },
		{ id: 'status', orderBy: 'DataOperationJobExecution.StatusId', numeric: false, disablePadding: true, label: 'Status' },
		// { id: 'log', orderBy: 'DataOperationJobExecution.Log', numeric: false, disablePadding: true, label: 'Log' },
		{ id: 'sourceDataCount', orderBy: 'SourceDataCount', numeric: false, disablePadding: true, label: 'Source Data Count' },
		{ id: 'affectedRowCount', orderBy: 'AffectedRowCount', numeric: false, disablePadding: true, label: 'Affected Row Count' },
		{ id: 'startDate', orderBy: 'DataOperationJobExecution.StartDate', numeric: false, disablePadding: true, label: 'Start Date' },
		{ id: 'endDate', orderBy: 'DataOperationJobExecution.EndDate', numeric: false, disablePadding: true, label: 'End Date' },
	];
	const [order, setOrder] = React.useState('desc');
	const [orderBy, setOrderBy] = React.useState('DataOperationJobExecution.Id');
	const [selected] = React.useState([]);
	const [page, setPage] = React.useState(1);
	const [rowsPerPage, setRowsPerPage] = React.useState(10);
	const dataOperationJobExecutionsList = useSelector(selectDataOperationJobExecutions);

	const totalCount = useSelector(({ dataOperationJobExecutionsApp }) => dataOperationJobExecutionsApp.dataOperationJobExecutions.count);
	const PageNumber = useSelector(({ dataOperationJobExecutionsApp }) => {
		if (page !== dataOperationJobExecutionsApp.dataOperationJobExecutions.pageNumber) {
			setPage(dataOperationJobExecutionsApp.dataOperationJobExecutions.pageNumber)
		}
		return dataOperationJobExecutionsApp.dataOperationJobExecutions.pageNumber
	});
	const PageSize = useSelector(({ dataOperationJobExecutionsApp }) => dataOperationJobExecutionsApp.dataOperationJobExecutions.pageSize);

	const routeParams = useParams();
	routeParams.PageNumber = PageNumber;
	routeParams.PageSize = PageSize === 0 ? 10 : PageSize;
	routeParams.OrderBy = orderBy;
	routeParams.Order = order;


	useEffect(() => {
		dispatch(getDataOperationJobExecutions(routeParams));
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
		
		dispatch(getDataOperationJobExecutions(routeParams));
	};

	const handleClick = (event, row) => {
	};

	const handleChangePage = (event, newPage) => {
		routeParams.PageSize = rowsPerPage;
		routeParams.PageNumber = newPage;
		dispatch(getDataOperationJobExecutions(routeParams));
		setPage(newPage);
	};

	const handleChangeRowsPerPage = event => {
		routeParams.PageSize = event.target.value;
		routeParams.PageNumber = page;

		dispatch(getDataOperationJobExecutions(routeParams));
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
							{stableSort(dataOperationJobExecutionsList, getComparator(order, orderBy)).map((dataOperationJobExecution, index) => {
								const isItemSelected = isSelected(dataOperationJobExecution.id);
								return (
									<StyledTableRow
										hover
										aria-checked={isItemSelected}
										tabIndex={-1}
										key={dataOperationJobExecution.id}
										selected={isItemSelected}
										onDoubleClick={event => handleClick(event, dataOperationJobExecution)}
									>
										<TableCell align="left">{dataOperationJobExecution.id}</TableCell>
										<TableCell align="left">{dataOperationJobExecution.jobId}</TableCell>
										<TableCell align="left">{dataOperationJobExecution.dataOperationName}</TableCell>
										<TableCell align="left">{dataOperationJobExecution.scheduleInfo.cron}({dataOperationJobExecution.scheduleInfo.startDate}-{dataOperationJobExecution.scheduleInfo.endDate})</TableCell>
										<TableCell align="left">{dataOperationJobExecution.statusDescription}</TableCell>
										{/* <TableCell align="left">{dataOperationJobExecution.log}</TableCell> */}
										<TableCell align="left">{dataOperationJobExecution.sourceDataCount}</TableCell>
										<TableCell align="left">{dataOperationJobExecution.affectedRowCount}</TableCell>
										<TableCell align="left">{dataOperationJobExecution.startDate}</TableCell>
										<TableCell align="left">{dataOperationJobExecution.endDate}</TableCell>
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

export default withRouter(DataOperationJobExecutionsData);
