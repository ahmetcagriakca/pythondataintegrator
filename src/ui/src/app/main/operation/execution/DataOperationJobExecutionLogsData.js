import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withRouter, useParams } from 'react-router-dom';
import { getDataOperationJobExecutionLogs, selectDataOperationJobExecutionLogs } from './store/dataOperationJobExecutionLogsSlice';
import StyledTableRow from '../../common/components/StyledTableRow';
import { tableStyles } from '../../common/styles/TableStyles';
import TableHead from '@material-ui/core/TableHead';
import TextField from '@material-ui/core/TextField';


function DataOperationJobExecutionLogsData(props) {
	const dispatch = useDispatch();
	const classes = tableStyles();
	const { ExecutionId } = props;
	const dataOperationJobExecutionLogsList = useSelector(selectDataOperationJobExecutionLogs);


	const routeParams = useParams();


	useEffect(() => {
		routeParams.ExecutionId = ExecutionId
		dispatch(getDataOperationJobExecutionLogs(routeParams));
	}, [dispatch, routeParams, ExecutionId]);


	return (
		<TableContainer className={classes.container} style={{ maxHeight: 650, borderTopLeftRadius: 30 }}>
			<Table stickyHeader aria-label="sticky table" size="small">
				<TableHead>
					<StyledTableRow key={'headRowIntegration'} className={classes.tableRowHeader}>
						<TableCell key={'headRowIntegrationDate'} align={'left'} padding={'normal'} className={classes.tableCell}> Date </TableCell>
						<TableCell key={'headRowIntegrationComment'} align={'left'} padding={'normal'} className={classes.tableCell}> Comment </TableCell>
						<TableCell key={'headRowIntegrationLog'} align={'left'} padding={'normal'} className={classes.tableCell}>  Log </TableCell>
					</StyledTableRow>
				</TableHead>
				<TableBody>
					{dataOperationJobExecutionLogsList.map((dataOperationJobExecutionLogs, index) => {
						return (
							<React.Fragment>
								<StyledTableRow
									hover
									key={dataOperationJobExecutionLogs.id}
								>
									<TableCell align="left">{dataOperationJobExecutionLogs.creationDate}</TableCell>
									<TableCell align="left">{dataOperationJobExecutionLogs.comments}</TableCell>
									<TableCell align="left">
										{/* {dataOperationJobExecutionLogs.content} */}
										<TextField
											id="outlined-textarea"
											value={dataOperationJobExecutionLogs.content}
											multiline
											minrows={1}
											maxrows={4}
											fullWidth={true}
											InputProps={{
												readOnly: true,
												className: classes.textarea
											}}
											style={{ width: 750 }}
											variant="outlined"
										/>

									</TableCell>
								</StyledTableRow>
							</React.Fragment>
						);
					})}
				</TableBody>
			</Table>
		</TableContainer>
	);
}

export default withRouter(DataOperationJobExecutionLogsData);
