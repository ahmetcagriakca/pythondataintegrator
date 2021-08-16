import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { selectConnectionName } from '../store/connectionNameSlice';
import DataIntegrationConnectionDatabaseContent from './DataIntegrationConnectionDatabaseContent';


const useStyles = makeStyles(theme => ({

}));

function DataIntegrationSourceConnectionContent(props) {
	const classes = useStyles();

	const { rowData, applyChange } = props;
	const [row, setRow] = React.useState(rowData);
	const checkValue = value => value ? value : ''

	const selectConnectionNames = useSelector(selectConnectionName);
	const filterOptions = createFilterOptions({
		matchFrom: 'any',
		stringify: option => {
			return option?.name
		},
	});
	useEffect(() => {
		setRow({ ...rowData })
	}, [rowData]);

	const handleConnectionChange = (event, value) => {
		let newRow = { ...row, connection: value }
		setRow(newRow);
		changeApply(newRow)
	};

	const changeApply = (newRow) => {
		if (newRow) {
			applyChange(newRow)
		} else {
			applyChange(row)
		}
	};

	const applyDataIntegrationConnectionDatabaseChange = (data) => {
		let newRow = { ...row, database: data }
		setRow(newRow);
		changeApply(newRow)
	};
	return (

		<Grid container spacing={1}>
			<Grid item xs={12}
				style={{ padding: '10px 0 0 0' }}>
				<Autocomplete
					id={"sourceConnection" + row?.id}
					style={{ width: '100%' }}
					value={row?.connection}
					onChange={(event, newValue) => {
						handleConnectionChange(event, newValue)
					}}
					options={selectConnectionNames}
					classes={{
						option: classes.option,
					}}
					filterOptions={filterOptions}
					getOptionLabel={(option) => checkValue(option?.name)}
					getOptionSelected={(option, value) => option?.id === value?.id}
					renderOption={(option) => (
						<React.Fragment>
							<span>{option?.name}</span>
						</React.Fragment>
					)}
					renderInput={(params) => (
						<TextField
							{...params}
							label="Connection"
							variant="outlined"
							inputProps={{
								...params.inputProps,
								autoComplete: 'new-password',
							}}
						/>
					)}
					autoHighlight
					clearOnEscape
					openOnFocus
				/>
			</Grid>

			{
				row?.connection?.connectionTypeId === 1 ?
					(
						<DataIntegrationConnectionDatabaseContent
							rowData={row.database}
							applyChange={applyDataIntegrationConnectionDatabaseChange}
						/>
					) : ('')
			}
		</Grid>
	);
}

export default DataIntegrationSourceConnectionContent;
