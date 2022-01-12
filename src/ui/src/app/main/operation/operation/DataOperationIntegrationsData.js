import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import Typography from '@material-ui/core/Typography';
import DataIntegrationContent from './integration/DataIntegrationContent';
import StyledTableCell from '../../common/components/StyledTableCell';
import StyledTableRow4n from '../../common/components/StyledTableRow4n';
import { uuid } from '../../common/utils/Utils';


const useStyles = makeStyles(theme => ({
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
	},

	tableHeadCellAction: {
		width: '5px',
		padding: '0px 8px',
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
	},
	tableBodyCellAction: {
		width: '5px',
		padding: '0px 8px',
		color: 'white',
		hover: {
			'&:hover': {
				backgroundColor: 'green !important'
			}
		}
	}
}));


function DataOperationIntegrationRow(props) {
	const { rowData, applyChange, rowIndex, deleteRow } = props;
	const [open, setOpen] = React.useState(false);
	const [row, setRow] = React.useState(rowData);
	const checkValue = value => value ? value : ''

	useEffect(() => {
		setRow({ ...rowData })
	}, [rowData]);

	const handleChange = (event, prop) => {
		setRow({ ...row, [prop]: event.target.type === 'number' ? (parseInt(event.target.value) || 0) : event.target.value });
	};

	const changeApply = (newRow) => {
		if (newRow) {
			applyChange(newRow, rowIndex)
		}
		else {
			applyChange(row, rowIndex)

		}
	};

	const applyDataIntegrationChange = (data) => {
		let newRow = { ...row, integration: data }
		setRow(newRow);
		changeApply(newRow)
	};

	return (
		<React.Fragment>
			<StyledTableRow4n key={'bodyRowIntegration' + row?.id}>
				<TableCell>
					<IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
						<Icon className="text-16 arrow-icon" color="inherit">
							{open ? 'expand_less' : 'expand_more'}
						</Icon>
					</IconButton>
				</TableCell>
				<StyledTableCell component="th" scope="row">{row?.integration?.code}</StyledTableCell>
				<StyledTableCell align="left">{row?.limit}</StyledTableCell>
				<StyledTableCell align="left">{row?.processCount}</StyledTableCell>
				<StyledTableCell align="left">{checkValue(row?.integration?.sourceConnection?.connection?.name)} </StyledTableCell>
				<StyledTableCell align="left">{checkValue(row?.integration?.targetConnection?.connection?.name)} </StyledTableCell>
				<StyledTableCell align="left">{row?.integration?.isTargetTruncate ? 'true' : 'false'}</StyledTableCell>
				<StyledTableCell align="left">{row?.integration?.comments}</StyledTableCell>

				<StyledTableCell >
					<IconButton aria-label="expand row" key={'cellIntegrationDeleteAction' + row?.id} size="small" onClick={event => deleteRow(event,row,rowIndex)}>
						<Icon className="text-16 arrow-icon" style={{ color: 'red' }}>
							remove_circle
						</Icon>
					</IconButton>
				</StyledTableCell>
			</StyledTableRow4n>
			<TableRow key={'bodyRowIntegrationBox' + row?.id}>
				<TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={12}>
					<Collapse in={open} key={'integrationBoxCollapse' + row?.id} timeout="auto" unmountOnExit>
						<Box key={'integrationBox' + row?.id}>
							<Grid container spacing={3}>
								<Grid item xs>
									<TextField
										id={"limit" + row?.id}
										label="Limit"
										type="number"
										fullWidth={true}
										InputLabelProps={{
											shrink: true,
										}}
										value={checkValue(row?.limit)}
										onChange={event => handleChange(event, 'limit')}
										onBlur={event => changeApply()}
									/>
								</Grid>
								<Grid item xs>
									<TextField
										id={"processCount" + row?.id}
										label="Process Count"
										type="number"
										fullWidth={true}
										InputLabelProps={{
											shrink: true,
										}}
										InputProps={{ inputProps: { min: 1, max: 10 } }}
										value={checkValue(row?.processCount)}
										onChange={event => handleChange(event, 'processCount')}
										onBlur={event => changeApply()}
									/>
								</Grid>
								<Grid item xs>
								</Grid>
								<Grid item xs>
								</Grid>
							</Grid>
							<Typography key={'integrationBoxTypography' + row?.id} variant="h6" gutterBottom component="div">
								Integration
							</Typography>
							<DataIntegrationContent rowData={row.integration} applyChange={applyDataIntegrationChange}></DataIntegrationContent>
						</Box>
					</Collapse>
				</TableCell>
			</TableRow>

		</React.Fragment>
	);
}

function DataOperationIntegrationsData(props) {
	const classes = useStyles();
	const { rowData, applyChange } = props;
	const [rows, setRows] = React.useState(rowData);
	useEffect(() => {
		setRows([...rowData])
	}, [rowData]);

	const changeApply = (newRows) => {
		if (newRows) {
			applyChange(newRows)
		} else {
			applyChange(rows)
		}
	};

	const deleteRow = (event, index,rowIndex) => {
		let tempRows = [...rows];
		tempRows.splice(rowIndex, 1)
		setRows(tempRows);
		changeApply(tempRows);
	}

	const addRow = (event) => {
		let tempRows = [...rows];
		tempRows = tempRows.concat({
			id: uuid(),
			limit: 0,
			processCount: 0,
			integration: {
				id: uuid(),
				code: '',
				isTargetTruncate: false,
				comments: '',
				sourceConnection: {
					id: uuid(),
					connection: {
						id: uuid(),
						database: {
							id: uuid(),
							connectorType: {
								id: uuid(),
							}
						},
						bigData: {
							id: uuid(),
							connectorType: {
								id: uuid(),
							}
						},
						connectionType: {
							id: uuid(),
						}
					},
					database: {
						id: uuid(),
					},
					bigData: {
						id: uuid(),
					}
				},
				targetConnection: {
					id: uuid(),
					connection: {
						id: uuid(),
						database: {
							id: uuid(),
							connectorType: {
								id: uuid(),
							}
						},
						bigData: {
							id: uuid(),
							connectorType: {
								id: uuid(),
							}
						},
						connectionType: {
							id: uuid(),
						}
					},
					database: {
						id: uuid(),
					},
					bigData: {
						id: uuid(),
					}
				},
				columns: [
				]
			}
		})
		setRows(tempRows);
		changeApply(tempRows);
	}

	const applyDataOperationIntegrationChange = (data, index) => {
		let tempRows = [...rows];
		let tempRow = {...rows[index]};
		tempRow = data
		tempRows[index]=tempRow
		setRows(tempRows);
		changeApply(tempRows);
	}

	return (

		<TableContainer className={classes.container} style={{ borderTopLeftRadius: 30 }}>
			<Table aria-label="sticky table" size="small">
				<caption>
					<IconButton aria-label="expand row" key={'cellIntegrationAddAction'} size="small" onClick={event => addRow(event)}>
						<Icon className="text-16 arrow-icon" style={{ color: 'green' }}>
							add_circle
						</Icon>
					</IconButton>
				</caption>
				<TableHead>
					<TableRow key={'headRowIntegration'} className={classes.tableRowHeader}>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}>  </StyledTableCell>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}> Code </StyledTableCell>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}> Limit </StyledTableCell>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}> Process Count </StyledTableCell>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}> Source Connection  </StyledTableCell>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}> Target Connection  </StyledTableCell>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}> Is Target Truncate </StyledTableCell>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}> Comments </StyledTableCell>
						<StyledTableCell align={'left'} padding={'normal'} className={classes.tableCell}> Action </StyledTableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{rows.map((row, rowIndex) => (
						<DataOperationIntegrationRow
							key={row.id}
							rowData={row}
							rowIndex={rowIndex}
							applyChange={applyDataOperationIntegrationChange}
							deleteRow={deleteRow}
						/>
					))}
				</TableBody>
			</Table>
		</TableContainer>
	);
}


export default DataOperationIntegrationsData;
