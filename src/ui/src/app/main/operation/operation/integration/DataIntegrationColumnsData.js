import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import StyledTableCell from '../../../common/components/StyledTableCell';
import StyledTableRow from '../../../common/components/StyledTableRow';
import { uuid } from '../../../common/utils/Utils';


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
	},
}));

function DataIntegrationColumnsData(props) {
	const classes = useStyles();

	const { rowData, applyChange } = props;
	const [rows, setRows] = React.useState(rowData);
	useEffect(() => {
		setRows([...rowData])
	}, [rowData]);
	const handleChange = (event, row, index, prop) => {
		let columns = [...rows];
		let column = { ...rows[index] };
		column[prop] = event.target.value
		columns[index] = column
		setRows(columns);
	};

	const changeApply = (newRows) => {
		if (newRows) {
			applyChange(newRows)
		} else {
			applyChange(rows)
		}
	};

	const deleteRow = (event, index) => {
		let tempRows = [...rows];
		tempRows.splice(index, 1)
		setRows(tempRows);
		changeApply(tempRows);
	}
	const addRow = (event) => {
		let tempRows = [...rows];
		tempRows = tempRows.concat({ id: uuid() })
		setRows(tempRows);
		changeApply(tempRows);
	}
	return (
		<Grid container spacing={3}>
			<Grid item xs={6} >
				<Box margin={1}>
					<Typography variant="h6" gutterBottom component="div">
						Source Columns
					</Typography>
					<Grid item xs={12}>
						{
							rows && rows !== null ? (
								<Table size="small" >
									<caption>
										<IconButton aria-label="expand row" key={'cellColumnAddAction'} size="small"
											onClick={event => addRow(event)}>
											<Icon className="text-16 arrow-icon" style={{ color: 'green' }}>
												add_circle
											</Icon>
										</IconButton>
									</caption>
									<TableHead>
										<TableRow key={'headRowIntegrationSourceColumns'} className={classes.tableRowHeader}>
											<TableCell key={'headCellIntegrationColumnAction'} align={'left'} padding={'normal'} className={classes.tableHeadCellAction}>  </TableCell>
											<TableCell key={'headCellIntegrationSourceColumnsColumn'} align={'left'} padding={'normal'} className={classes.tableCell}> Name </TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{rows?.map((row, rowIndex) => (
											<StyledTableRow key={'bodyRowIntegrationSourceColumn' + row?.id}>
												<StyledTableCell className={classes.tableBodyCellAction}>
													<IconButton
														key={'cellColumnDeleteAction' + row?.id}
														size="small"
														aria-label="expand row"
														onClick={event => deleteRow(event, rowIndex)}>
														<Icon className="text-16 arrow-icon" style={{ color: 'red' }}>
															remove_circle
														</Icon>
													</IconButton>
												</StyledTableCell>
												<StyledTableCell>

													<TextField
														key={'bodyCellTextIntegrationSourceColumnName' + row?.id}
														id={'bodyCellTextIntegrationSourceColumnName' + row?.id}
														label=""
														fullWidth={true}
														InputLabelProps={{ shrink: false }}
														value={row?.sourceColumnName}
														onChange={event => handleChange(event, row, rowIndex, 'sourceColumnName')}
														onBlur={event => changeApply()}
													/>
												</StyledTableCell>
											</StyledTableRow>
										))}
									</TableBody>
								</Table>
							) : ("")
						}
					</Grid>
				</Box>
			</Grid>
			<Grid item xs={6} >
				<Box margin={1}>
					<Typography variant="h6" gutterBottom component="div">
						Target Columns
					</Typography>
					<Grid item xs={12}>
						{
							rows && rows !== null ? (
								<Table size="small" >
									<TableHead>
										<TableRow key={'headRowIntegrationTargetColumns'} className={classes.tableRowHeader}>
											<TableCell key={'headCellIntegrationTargetColumnsColumn'} align={'left'} padding={'normal'} className={classes.tableCell}> Name </TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{rows?.map((row, rowIndex) => (
											<StyledTableRow key={'bodyRowIntegrationTargetColumn' + row?.id}>
												<StyledTableCell key={'bodyCellIntegrationTargetColumnName' + row?.id} >
													<TextField
														key={'bodyCellTextIntegrationTargetColumnName' + row?.id}
														id={'bodyCellTextIntegrationTargetColumnName' + row?.id}
														label=""
														fullWidth={true}
														InputLabelProps={{ shrink: false }}
														value={row?.targetColumnName}
														onChange={event => handleChange(event, row, rowIndex, 'targetColumnName')}
														onBlur={event => changeApply()}
													/>
												</StyledTableCell>
											</StyledTableRow>
										))}
									</TableBody>
								</Table>
							) : ("")
						}
					</Grid>
				</Box>
			</Grid>
		</Grid>
	);
}

export default DataIntegrationColumnsData;
