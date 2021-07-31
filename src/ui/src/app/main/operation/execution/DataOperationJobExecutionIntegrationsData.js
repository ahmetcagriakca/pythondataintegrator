import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import { getDataOperationJobExecutionIntegrations, selectDataOperationJobExecutionIntegrations } from './store/dataOperationJobExecutionIntegrationsSlice';
import StyledTableRow from '../../common/components/StyledTableRow';
import { tableStyles } from '../../common/styles/TableStyles';
import TableHead from '@material-ui/core/TableHead';


function DataOperationJobExecutionIntegrationsData(props) {
	const dispatch = useDispatch();
	const classes = tableStyles();
	const dataOperationJobExecutionIntegrationsList = useSelector(selectDataOperationJobExecutionIntegrations);


	const routeParams = useParams();
	routeParams.ExecutionId = props.ExecutionId


	useEffect(() => {
		dispatch(getDataOperationJobExecutionIntegrations(routeParams));
	}, [dispatch, routeParams]);


	return (
		<TableContainer className={classes.container} style={{ maxHeight: 650, borderTopLeftRadius: 30 }}>
			<Table stickyHeader aria-label="sticky table" size="small">
				<TableHead>
					<StyledTableRow key={'headRowIntegration'} className={classes.tableRowHeader}>
						<TableCell key={'headRowIntegrationOrder'} align={'left'} padding={'normal'} className={classes.tableCell}> Order </TableCell>
						<TableCell key={'headRowIntegrationCode'} align={'left'} padding={'normal'} className={classes.tableCell}> Code </TableCell>
						<TableCell key={'headRowIntegrationStatus'} align={'left'} padding={'normal'} className={classes.tableCell}> Status </TableCell>
						<TableCell key={'headRowIntegrationSourceConnection'} align={'left'} padding={'normal'} className={classes.tableCell}>  Source Connection  </TableCell>
						<TableCell key={'headRowIntegrationTargetConnection'} align={'left'} padding={'normal'} className={classes.tableCell}> Target Connection   </TableCell>
						<TableCell key={'headRowIntegrationLimit'} align={'left'} padding={'normal'} className={classes.tableCell}> Limit  </TableCell>
						<TableCell key={'headRowIntegrationProcessCount'} align={'left'} padding={'normal'} className={classes.tableCell}> Process Count </TableCell>
						<TableCell key={'headRowIntegrationSourceDataCount'} align={'left'} padding={'normal'} className={classes.tableCell}> Source Data Count </TableCell>
						<TableCell key={'headRowIntegrationAffectedRowCount'} align={'left'} padding={'normal'} className={classes.tableCell}> Affected Row Count </TableCell>
						<TableCell key={'headRowIntegrationComments'} align={'left'} padding={'normal'} className={classes.tableCell}> Start Date </TableCell>
					</StyledTableRow>
				</TableHead>
				<TableBody>
					{dataOperationJobExecutionIntegrationsList.map((dataOperationJobExecutionIntegrations, index) => {
						return (
							<React.Fragment>
								<StyledTableRow
									hover
									key={dataOperationJobExecutionIntegrations.id}
								>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.order}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.dataIntegrationCode}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.status}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.sourceConnectionName}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.targetConnectionName}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.limit}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.processCount}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.sourceDataCount}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.affectedRowCount}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionIntegrations.startDate}</TableCell>
								</StyledTableRow>
							</React.Fragment>
						);
					})}
				</TableBody>
			</Table>
		</TableContainer>
	);
}

export default withRouter(DataOperationJobExecutionIntegrationsData);
