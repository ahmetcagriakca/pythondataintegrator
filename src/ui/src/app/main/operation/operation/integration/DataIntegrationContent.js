import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import DataIntegrationSourceConnectionContent from './DataIntegrationSourceConnectionContent';
import DataIntegrationTargetConnectionContent from './DataIntegrationTargetConnectionContent';
import DataIntegrationColumnsData from './DataIntegrationColumnsData';


const useStyles = makeStyles(theme => ({
	divider: {
		margin: theme.spacing(2, 0),
	},
}));


function DataIntegrationContent(props) {
	const classes = useStyles();

	const { rowData, applyChange } = props;
	const [row, setRow] = React.useState(rowData);
	const checkValue = value => value ? value : ''

	useEffect(() => {
		setRow({ ...rowData })
	}, [rowData]);

	const handleIsTargetTruncateChange = (event, value) => {
		let newRow = { ...row, isTargetTruncate: value }
		setRow(newRow);
		changeApply(newRow)
	};

	const handleChange = (event, prop) => {
		setRow({ ...row, [prop]: event.target.type === 'number' ? (parseInt(event.target.value) || 0) : event.target.value });
	};

	const changeApply = (newRow) => {
		if (newRow) {
			applyChange(newRow)
		} else {
			applyChange(row)
		}
	};

	const applyDataIntegrationSourceConnectionChange = (data) => {
		let newRow = { ...row, sourceConnection: data }
		setRow(newRow);
		changeApply(newRow)
	};

	const applyDataIntegrationTargetConnectionChange = (data) => {
		let newRow = { ...row, targetConnection: data }
		setRow(newRow);
		changeApply(newRow)
	};
	const applyDataIntegrationColumnsChange = (data) => {
		let newRow = { ...row, columns: data }
		setRow(newRow);
		changeApply(newRow)
	};

	return (
		<Box>
			<Grid container spacing={3}>
				<Grid item xs>
					<TextField
						id={"code" + row?.id}
						label="Code"
						fullWidth={true}
						InputLabelProps={{
							shrink: true,
						}}
						value={checkValue(row?.code)}
						onChange={event => handleChange(event, 'code')}
						onBlur={event => changeApply()}
					/>
				</Grid>
				<Grid item xs>

					<FormControlLabel
						id={"isTargetTruncate" + row?.id}
						style={{ margin: "5px" }}
						control={
							<Checkbox
								name="isTargetTruncate"
								checked={row?.isTargetTruncate}
								onChange={(event, newValue) => {
									handleIsTargetTruncateChange(event, newValue);
								}} />
						}
						label="Is Target Truncate"
					/>
				</Grid>
				<Grid item xs>
					<TextField
						id={"comments" + row?.id}
						label="Comments"
						fullWidth={true}
						InputLabelProps={{
							shrink: true,
						}}
						value={checkValue(row?.comments)}
						onChange={event => handleChange(event, 'comments')}
						onBlur={event => changeApply()}
					/>
				</Grid>
				<Grid item xs>
				</Grid>
			</Grid>
			<Divider className={classes.divider} />
			<Grid container spacing={3}>

				<Grid item xs={6} >
					<Box margin={1}>
						<Typography variant="h6" gutterBottom component="div">
							Source Connection
						</Typography>

						<DataIntegrationSourceConnectionContent
							key={"sourceConncetion" + row.id}
							rowData={row?.sourceConnection}
							applyChange={applyDataIntegrationSourceConnectionChange}
						/>
					</Box>
				</Grid>
				<Grid item style={{ margin: "0 0 0 5" }} xs={6} >
					<Box margin={1}>
						<Typography variant="h6" gutterBottom component="div">
							Target Connection
						</Typography>
						<DataIntegrationTargetConnectionContent
							key={"targetConnection" + row.id}
							rowData={row?.targetConnection}
							applyChange={applyDataIntegrationTargetConnectionChange}
						/>
					</Box>
				</Grid>
			</Grid>
			{
				row?.sourceConnection && row?.sourceConnection != null && row?.sourceConnection?.connection?.name != null && row?.targetConnection && row?.targetConnection != null && row?.targetConnection?.connection?.name != null ?
					(
						<DataIntegrationColumnsData
							key={"targetConnection" + row.id}
							rowData={row?.columns}
							applyChange={applyDataIntegrationColumnsChange}
						/>
					) : ('')
			}
		</Box>
	)
}

export default DataIntegrationContent;
