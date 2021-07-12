import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import TableContainer from '@material-ui/core/TableContainer';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import React, { useEffect } from 'react';
import clsx from 'clsx';
import { useDispatch, useSelector } from 'react-redux';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import { withRouter, useParams } from 'react-router-dom';
import Icon from '@material-ui/core/Icon';
import { getConnections, selectConnections } from './store/connectionsSlice';
import CustomPagination from '../../common/components/CustomPagination';


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
							onClick={createSortHandler(headCell.orderBy)}
						>
							{headCell.label}
						</TableSortLabel>
					</TableCell>
				))}
			</TableRow>
		</TableHead>
	);
}
function ConnectionsData() {
	const dispatch = useDispatch();
	const classes = useStyles();
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
		dispatch(getConnections(routeParams));
	};

	const handleClick = (event, connectionName) => {
		const message = connectionName.concat(' isimli connection git');
		alert(message);
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
						<EnhancedTableHead order={order} orderBy={orderBy} onRequestSort={handleRequestSort} />
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
										onDoubleClick={event => handleClick(event, connection.name)}
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
										<TableCell align="left">
											<div
												style={{
													display: 'flex',
													alignItems: 'center',
													flexWrap: 'wrap'
												}}
											>
												{connection.monitoringStatus === 'Monitoring' ? (
													<Icon className="text-green text-20">check_circle</Icon>
												) : connection.monitoringStatus === 'Timeout' ? (
													<Icon className="text-yellow text-20">access_time</Icon>
												) : (
													<Icon className="text-red text-20">remove_circle</Icon>
												)}
												<span>{connection.monitoringStatus}</span>
											</div>
										</TableCell>
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
