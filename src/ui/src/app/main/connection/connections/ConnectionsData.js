import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import Paper from '@material-ui/core/Paper';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import clsx from 'clsx';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import { getConnections, selectConnections } from './store/connectionsSlice';
import CustomPagination from '../../common/components/CustomPagination';
import EnhancedTableHead from '../../common/components/EnhancedTableHead';
import StyledTableRow from '../../common/components/StyledTableRow';
import { stableSort, getComparator } from '../../common/utils/TableUtils';
import { tableStyles } from '../../common/styles/TableStyles';
import { useHistory } from 'react-router-dom';


function ConnectionsData() {
	const dispatch = useDispatch();
	const classes = tableStyles();
	const history = useHistory();
	const headCells = [
		{ id: 'connectionId', orderBy: 'Connection.Id', connectionId: 'connectionId', numeric: true, disablePadding: true, label: 'Id' },
		{ id: 'connectionName', orderBy: 'Connection.Name', name: 'connectionName', numeric: false, disablePadding: true, label: 'Name' },
		{ id: 'connectionTypeName', orderBy: 'ConnectionType.Name', connectionTypeName: 'connectionTypeName', numeric: false, disablePadding: true, label: 'Connection Type' },
		{ id: 'connectorTypeName', orderBy: 'ConnectorType.Name', connectorTypeName: 'connectorTypeName', numeric: false, disablePadding: true, label: 'Connector Type' },
		{ id: 'host', orderBy: 'ConnectionServer.Host', host: 'host', numeric: false, disablePadding: true, label: 'Host' },
		{ id: 'port', orderBy: 'ConnectionServer.Host', port: 'port', numeric: true, disablePadding: true, label: 'Port' },
		{ id: 'sid', orderBy: 'ConnectionDatabase.Sid', sid: 'sid', numeric: false, disablePadding: true, label: 'Sid' },
		{ id: 'serviceName', orderBy: 'ConnectionDatabase.ServiceName', serviceName: 'serviceName', numeric: false, disablePadding: true, label: 'Service Name' },
		{ id: 'databaseName', orderBy: 'ConnectionDatabase.DatabaseName', databaseName: 'databaseName', numeric: false, disablePadding: true, label: 'DatabaseName' },
		{ id: 'creationDate', orderBy: 'Connection.CreationDate', creationDate: 'creationDate', numeric: false, disablePadding: true, label: 'CreationDate' },
		{ id: 'action', Action: 'Action', numeric: false }
	];
	const [order, setOrder] = React.useState('asc');
	const [orderBy, setOrderBy] = React.useState('Connection.Id');
	const [selected] = React.useState([]);
	const [page, setPage] = React.useState(1);
	const [rowsPerPage, setRowsPerPage] = React.useState(10);
	const connectionsList = useSelector(selectConnections);

	const totalCount = useSelector(({ connectionsApp }) => connectionsApp.connections.count);
	const PageNumber = useSelector(({ connectionsApp }) => {
		if (page !== connectionsApp.connections.pageNumber) {
			setPage(connectionsApp.connections.pageNumber)
		}
		return connectionsApp.connections.pageNumber
	});
	const PageSize = useSelector(({ connectionsApp }) => connectionsApp.connections.pageSize);

	const routeParams = useParams();
	routeParams.PageNumber = PageNumber;
	routeParams.PageSize = PageSize === 0 ? 10 : PageSize;
	routeParams.OrderBy = orderBy;
	routeParams.Order = order;

	useEffect(() => {
		dispatch(getConnections(routeParams));
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
		dispatch(getConnections(routeParams));
	};

	function GotoComponent(path) {
		history.push('/'.concat(path));
	}
	const handleClick = (event, connection) => {
		GotoComponent('connection/'+connection.id)
	};

	const handleChangePage = (event, newPage) => {
		routeParams.PageSize = rowsPerPage;
		routeParams.PageNumber = newPage;
		dispatch(getConnections(routeParams));
		setPage(newPage);
	};

	const handleChangeRowsPerPage = event => {
		routeParams.PageSize = event.target.value;
		routeParams.PageNumber = page;

		dispatch(getConnections(routeParams));
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
							{stableSort(connectionsList, getComparator(order, orderBy)).map((connection, index) => {
								const isItemSelected = isSelected(connection.id);
								return (
									<StyledTableRow
										hover
										aria-checked={isItemSelected}
										tabIndex={-1}
										key={connection.id}
										selected={isItemSelected}
										onDoubleClick={event => handleClick(event, connection)}
									>
										<TableCell align="left">{connection.id}</TableCell>
										<TableCell align="left">{connection.name}</TableCell>
										<TableCell align="left">{connection.connectionTypeName}</TableCell>
										<TableCell align="left">{connection.connectorTypeName}</TableCell>
										<TableCell align="left">{connection.host}</TableCell>
										<TableCell align="left">{connection.port}</TableCell>
										<TableCell align="left">{connection.sid}</TableCell>
										<TableCell align="left">{connection.serviceName}</TableCell>
										<TableCell align="left">{connection.databaseName}</TableCell>
										<TableCell align="left">{connection.creationDate}</TableCell>
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

export default withRouter(ConnectionsData);
