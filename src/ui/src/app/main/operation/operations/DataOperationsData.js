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
import Typography from '@material-ui/core/Typography';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import { getDataOperations, selectDataOperations } from './store/dataOperationsSlice';
import CustomPagination from '../../common/components/CustomPagination';
import EnhancedTableHead from '../../common/components/EnhancedTableHead';
import StyledTableRow from '../../common/components/StyledTableRow';
import { stableSort, getComparator } from '../../common/utils/TableUtils';
import { tableStyles } from '../../common/styles/TableStyles';
import { useHistory } from 'react-router-dom';

function DataOperationsRow(props) {
	const { row, isItemSelected } = props;
	const [open, setOpen] = React.useState(false);
	const history = useHistory();

	function GotoComponent(path) {
		history.push('/'.concat(path));
	}
	const handleClick = (event, row) => {
		GotoComponent('operation/' + row.id)
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
				<TableCell align="left">{row.definitionId}</TableCell>
				<TableCell align="left">{row.creationDate}</TableCell>
				<TableCell align="left">{row.isDeleted}</TableCell>
			</StyledTableRow>
			<TableRow>
				<TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
					<Collapse in={open} timeout="auto" unmountOnExit>
						<Box margin={1}>
							<Typography variant="h4" gutterBottom component="div">
								Contacts
							</Typography>
							{
								row.contacts !== null ? (
									<Table size="small" >
										<TableHead>
											<TableRow >
												<TableCell align={'left'} padding={'normal'} > Email </TableCell>
											</TableRow>
										</TableHead>
										<TableBody>
											{row.contacts.map((contactRow) => (
												<TableRow key={contactRow.id}>
													<TableCell>{contactRow.email}</TableCell>
												</TableRow>
											))}
										</TableBody>
									</Table>
								) :
									("")
							}
						</Box>
					</Collapse>
				</TableCell>
			</TableRow>
		</React.Fragment>
	);
}

function DataOperationsData() {
	const dispatch = useDispatch();
	const classes = tableStyles();
	const headCells = [
		{ id: 'collapse', orderBy: null, numeric: false, disablePadding: true, label: '' },
		{ id: 'id', orderBy: 'DataOperation.Id', numeric: false, disablePadding: true, label: 'Id' },
		{ id: 'name', orderBy: 'DataOperation.Name', numeric: false, disablePadding: true, label: 'Name' },
		{ id: 'definitionId', orderBy: 'Definition.Id', numeric: false, disablePadding: true, label: 'Definition Id' },
		{ id: 'creationDate', orderBy: 'DataOperation.CreationDate', numeric: false, disablePadding: true, label: 'Creation Date' },
		{ id: 'isDeleted', orderBy: 'DataOperation.IsDeleted', numeric: false, disablePadding: true, label: 'Is Deleted' },
	];
	const [order, setOrder] = React.useState('desc');
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
		routeParams.OnlyUndeleted = true;
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
		<Paper style={{ borderTopLeftRadius: 30 }} className={classes.paper}>
			<TableContainer className={classes.container} style={{ maxHeight: 650, borderTopLeftRadius: 30 }}>
				<Table stickyHeader aria-label="sticky table" size="small">
					<EnhancedTableHead order={order} orderBy={orderBy} onRequestSort={handleRequestSort} headCells={headCells} />
					<TableBody>
						{stableSort(dataOperationsList, getComparator(order, orderBy)).map((dataOperation, index) => {
							const isItemSelected = isSelected(dataOperation.id);
							return (
								<DataOperationsRow key={dataOperation.id} row={dataOperation} isItemSelected={isItemSelected} />
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

export default withRouter(DataOperationsData);
