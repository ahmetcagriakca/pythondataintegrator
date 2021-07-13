import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import Paper from '@material-ui/core/Paper';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import clsx from 'clsx';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import { getDataOperationJobs, selectDataOperationJobs } from './store/dataOperationJobsSlice';
import CustomPagination from '../../common/components/CustomPagination';
import EnhancedTableHead from '../../common/components/EnhancedTableHead';
import StyledTableRow from '../../common/components/StyledTableRow';
import { stableSort, getComparator } from '../../common/utils/TableUtils';
import { tableStyles } from '../../common/styles/TableStyles';

function DataOperationJobsData() {
	const dispatch = useDispatch();
	const classes = tableStyles();
	const headCells = [
		{ id: 'id', orderBy: 'DataOperationJob.Id', numeric: true, disablePadding: true, label: 'Id' },
		{ id: 'jobId', orderBy: 'ApSchedulerJob.Id', numeric: true, disablePadding: true, label: 'Job Id' },
		{ id: 'dataOperationName', orderBy: 'DataOperation.Name', numeric: false, disablePadding: true, label: 'Name' },
		{ id: 'cron', orderBy: 'DataOperationJob.Cron', numeric: false, disablePadding: true, label: 'Cron' },
		{ id: 'startDate', orderBy: 'DataOperationJob.StartDate', numeric: false, disablePadding: true, label: 'Start Date' },
		{ id: 'EndDate', orderBy: 'DataOperationJob.EndDate', numeric: false, disablePadding: true, label: 'End Date' },
		{ id: 'nextRunTime', orderBy: 'ApSchedulerJob.NextRunTime', numeric: false, disablePadding: true, label: 'Next Run Time' },
		{ id: 'creationDate', orderBy: 'DataOperationJob.CreationDate', numeric: false, disablePadding: true, label: 'Creation Date' },
		{ id: 'isDeleted', orderBy: 'DataOperationJob.IsDeleted', numeric: false, disablePadding: true, label: 'Is Deleted' },
	];
	const [order, setOrder] = React.useState('desc');
	const [orderBy, setOrderBy] = React.useState('DataOperationJob.Id');
	const [selected] = React.useState([]);
	const [page, setPage] = React.useState(1);
	const [rowsPerPage, setRowsPerPage] = React.useState(10);
	const dataOperationJobsList = useSelector(selectDataOperationJobs);

	const totalCount = useSelector(({ dataOperationJobsApp }) => dataOperationJobsApp.dataOperationJobs.count);
	const PageNumber = useSelector(({ dataOperationJobsApp }) => {
		if (page !== dataOperationJobsApp.dataOperationJobs.pageNumber) {
			setPage(dataOperationJobsApp.dataOperationJobs.pageNumber)
		}
		return dataOperationJobsApp.dataOperationJobs.pageNumber
	});
	const PageSize = useSelector(({ dataOperationJobsApp }) => dataOperationJobsApp.dataOperationJobs.pageSize);

	const routeParams = useParams();
	routeParams.PageNumber = PageNumber;
	routeParams.PageSize = PageSize === 0 ? 10 : PageSize;
	routeParams.OrderBy = orderBy;
	routeParams.Order = order;


	useEffect(() => {
		routeParams.OnlyCron = true;
		routeParams.OnlyUndeleted = true;
		dispatch(getDataOperationJobs(routeParams));
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
		
		dispatch(getDataOperationJobs(routeParams));
	};

	const handleClick = (event, row) => {
		const message = row.id + ' isimli dataOperationJob git';
		alert(message);
	};

	const handleChangePage = (event, newPage) => {
		routeParams.PageSize = rowsPerPage;
		routeParams.PageNumber = newPage;
		dispatch(getDataOperationJobs(routeParams));
		setPage(newPage);
	};

	const handleChangeRowsPerPage = event => {
		routeParams.PageSize = event.target.value;
		routeParams.PageNumber = page;

		dispatch(getDataOperationJobs(routeParams));
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
							{stableSort(dataOperationJobsList, getComparator(order, orderBy)).map((dataOperationJob, index) => {
								const isItemSelected = isSelected(dataOperationJob.id);
								return (
									<StyledTableRow
										hover
										aria-checked={isItemSelected}
										tabIndex={-1}
										key={dataOperationJob.id}
										selected={isItemSelected}
										onDoubleClick={event => handleClick(event, dataOperationJob)}
									>

										<TableCell align="left">{dataOperationJob.id}</TableCell>
										<TableCell align="left">{dataOperationJob.jobId}</TableCell>
										<TableCell align="left">{dataOperationJob.dataOperationName}</TableCell>
										<TableCell align="left">{dataOperationJob.cron}</TableCell>
										<TableCell align="left">{dataOperationJob.startDate}</TableCell>
										<TableCell align="left">{dataOperationJob.endDate}</TableCell>
										<TableCell align="left">{dataOperationJob.nextRunTime}</TableCell>
										<TableCell align="left">{dataOperationJob.creationDate}</TableCell>
										<TableCell align="left">{dataOperationJob.isDeleted}</TableCell>
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

export default withRouter(DataOperationJobsData);
