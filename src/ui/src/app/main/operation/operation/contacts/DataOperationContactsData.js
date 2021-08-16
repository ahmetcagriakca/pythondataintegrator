import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableContainer from '@material-ui/core/TableContainer';
import React, { useEffect } from 'react';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
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
	}
}));

function DataOperationContactsData(props) {
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
		<TableContainer className={classes.container} style={{ maxHeight: 650, borderTopLeftRadius: 30 }}>
			<Table stickyHeader aria-label="sticky table" size="small">
				<caption>
					<IconButton aria-label="expand row" key={'cellContactAddAction'} size="small" onClick={event => addRow(event)}>
						<Icon className="text-16 arrow-icon" style={{ color: 'green' }}>
							add_circle
						</Icon>
					</IconButton>
				</caption>
				<TableHead>
					<TableRow key={'headRowContact'} className={classes.tableRowHeader}>
						<StyledTableCell key={'headCellContactEmail'} align={'left'} padding={'normal'} className={classes.tableCell}> Email </StyledTableCell>
						<StyledTableCell key={'headCellContactAction'} align={'left'} padding={'normal'} className={classes.tableHeadCellAction}> Action </StyledTableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{rows.map((row, rowIndex) => (
						<StyledTableRow key={'bodyRowContact' + row?.id}>
							<StyledTableCell key={'bodyCellContactEmail' + row?.id} >

								<TextField
									id={'email' + row?.id}
									label=""
									InputLabelProps={{ shrink: false }}
									fullWidth={true}
									value={row?.email}
									onChange={event => handleChange(event, row, rowIndex, 'email')}
									onBlur={event => changeApply()}
								/>
							</StyledTableCell>
							<StyledTableCell key={'bodyCellContactDeleteAction' + row?.id} className={classes.tableBodyCellAction}>
								<IconButton aria-label="expand row" key={'cellContactDeleteAction' + row?.id} size="small"
									onClick={event => deleteRow(event, row, rowIndex)}>
									<Icon className="text-16 arrow-icon" style={{ color: 'red' }}>
										remove_circle
									</Icon>
								</IconButton>
							</StyledTableCell>
						</StyledTableRow>
					))}
				</TableBody>
			</Table>
		</TableContainer>
	);
}
export default DataOperationContactsData