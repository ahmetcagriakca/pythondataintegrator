import React, { useEffect } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import TableHead from '@material-ui/core/TableHead';
import Paper from '@material-ui/core/Paper';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import Collapse from '@material-ui/core/Collapse';
import Box from '@material-ui/core/Box';
import TableContainer from '@material-ui/core/TableContainer';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import { getConnections, selectConnections } from './store/connectionsSlice';
import CustomPagination from '../../common/components/CustomPagination';
import EnhancedTableHead from '../../common/components/EnhancedTableHead';
import StyledTableRow from '../../common/components/StyledTableRow';
import { stableSort, getComparator } from '../../common/utils/TableUtils';
import { tableStyles } from '../../common/styles/TableStyles';
import { useHistory } from 'react-router-dom';

function ConnectionsRow(props) {
	const { row, isItemSelected } = props;
	const [open, setOpen] = React.useState(false);
	const history = useHistory();

	function GotoComponent(path) {
		history.push('/'.concat(path));
	}
	const handleClick = (event, row) => {
		GotoComponent('connection/' + row.id)
	};
	return (
		<React.Fragment>
			<StyledTableRow
				hover
				aria-checked={isItemSelected}
				tabIndex={-1}
				key={row.id}
				selected={isItemSelected}
				onDoubleClick={event => handleClick(event, row)}
			>
				<TableCell>
					<IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
						<Icon className="text-16 arrow-icon" color="inherit">
							{open ? 'expand_less' : 'expand_more'}
						</Icon>
					</IconButton>
				</TableCell>
				<TableCell align="left">{row.id}</TableCell>
				<TableCell align="left">{row.name}</TableCell>
				<TableCell align="left">{row.connectionType.name}</TableCell>
				<TableCell align="left">{row.connectorType.name}</TableCell>
				<TableCell align="left">{row.creationDate}</TableCell>
				<TableCell align="left">{row.isDeleted}</TableCell>
			</StyledTableRow>
			<TableRow>
				<TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
					<Collapse in={open} timeout="auto" unmountOnExit>
						<Box margin={1}>
							{
								row.connectionType.id === 1 ? (
									<Table>
										<TableHead>
											<TableRow >
												<TableCell align={'left'} padding={'normal'} > Host </TableCell>
												<TableCell align={'left'} padding={'normal'} > Port </TableCell>
												{
													row.connectorType.id === 2 ? (
														<TableCell align={'left'} padding={'normal'} > Sid </TableCell>
													) : ('')
												}
												{
													row.connectorType.id === 2 ? (
														<TableCell align={'left'} padding={'normal'} > Service Name </TableCell>
													) : ('')
												}
												{
													row.connectorType.id !== 2 ? (
														<TableCell align={'left'} padding={'normal'} > Database Name </TableCell>
													) : ('')
												}
											</TableRow>
										</TableHead>
										<TableBody>
											<TableRow >
												<TableCell align="left">{row.host}</TableCell>
												<TableCell align="left">{row.port}</TableCell>
												{
													row.connectorType.id === 2 ? (
														<TableCell align="left">{row.sid}</TableCell>
													) : ('')
												}
												{
													row.connectorType.id === 2 ? (
														<TableCell align="left">{row.serviceName}</TableCell>
													) : ('')
												}
												{
													row.connectorType.id !== 2 ? (
														<TableCell align="left">{row.databaseName}</TableCell>
													) : ('')
												}
											</TableRow >
										</TableBody>
									</Table>
								) : (
									<Table>
										<TableHead>
											<TableRow >
												<TableCell align={'left'} padding={'normal'} > Host </TableCell>
												<TableCell align={'left'} padding={'normal'} > Port </TableCell>
											</TableRow>
										</TableHead>
										<TableBody>
											<TableRow >
												<TableCell align="left">{row.host}</TableCell>
												<TableCell align="left">{row.port}</TableCell>
											</TableRow >
										</TableBody>
									</Table>
								)
							}
						</Box>
					</Collapse>
				</TableCell>
			</TableRow>
		</React.Fragment>
	);
}


function ConnectionsData() {
	const dispatch = useDispatch();
	const classes = tableStyles();
	const headCells = [
		{ id: 'collapse', orderBy: null, numeric: false, disablePadding: true, label: '' },
		{ id: 'connectionId', orderBy: 'Connection.Id', numeric: false, disablePadding: true, label: 'Id' },
		{ id: 'connectionName', orderBy: 'Connection.Name', numeric: false, disablePadding: true, label: 'Name' },
		{ id: 'connectionTypeName', orderBy: 'ConnectionType.Name', numeric: false, disablePadding: true, label: 'Connection Type' },
		{ id: 'connectorTypeName', orderBy: 'ConnectorType.Name', numeric: false, disablePadding: true, label: 'Connector Type' },
		{ id: 'creationDate', orderBy: 'Connection.CreationDate', creationDate: 'creationDate', numeric: false, disablePadding: true, label: 'CreationDate' },
		{ id: 'isDeleted', orderBy: 'Connection.IsDeleted', numeric: false, disablePadding: true, label: 'Is Deleted' },
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
		routeParams.OnlyUndeleted = true;
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
			<Paper style={{ borderTopLeftRadius: 30 }} className={classes.paper}>
				<TableContainer className={classes.container} style={{ maxHeight: 650, borderTopLeftRadius: 30 }}>
					<Table stickyHeader aria-label="sticky table" size="small">
						<EnhancedTableHead order={order} orderBy={orderBy} onRequestSort={handleRequestSort} headCells={headCells} />
						<TableBody>
							{stableSort(connectionsList, getComparator(order, orderBy)).map((connection, index) => {
								const isItemSelected = isSelected(connection.id);
								return (
									<ConnectionsRow key={connection.id} row={connection} isItemSelected={isItemSelected} />
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
	);
}

export default withRouter(ConnectionsData);
