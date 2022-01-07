import React, { useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';


const useStyles = makeStyles(theme => ({
	textarea: {
		resize: "both",
	},
}));

function DataIntegrationConnectionBigDataContent(props) {
	const classes = useStyles();
	const { rowData, applyChange } = props;
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
			applyChange(newRow)
		} else {
			applyChange(row)
		}
	};
	return (

		<Box style={{ width: '100%', padding: '10px 0 0 0' }}>

			<Grid container>
				<Grid item xs={6}>
					<TextField
						id={"schema" + row?.id}
						label="Schema"
						variant="outlined"
						fullWidth={true}
						InputLabelProps={{
							shrink: true,
						}}
						value={checkValue(row?.schema)}
						onChange={event => handleChange(event, 'schema')}
						onBlur={event => changeApply()}
					/>
				</Grid>
				<Grid item xs={6}
					style={{ padding: '0 0 0 5px' }}>
					<TextField
						id={"table" + row?.id}
						label="Table"
						variant="outlined"
						fullWidth={true}
						InputLabelProps={{
							shrink: true,
						}}
						value={checkValue(row?.tableName)}
						onChange={event => handleChange(event, 'tableName')}
						onBlur={event => changeApply()}
					/>
				</Grid>
				<Grid item xs={12}
					style={{ padding: '10px 0 0 0' }}>
					<TextField
						id={"query" + row?.id}
						label="Query"
						placeholder="Query"
						multiline
						minrows={4}
						maxrows={4}
						fullWidth={true}
						variant="outlined"
						inputProps={{ className: classes.textarea }}
						value={checkValue(row.query)}
						onChange={event => handleChange(event, 'query')}
						onBlur={event => changeApply()}
					/>
				</Grid>
			</Grid>
		</Box>
	);
}

export default DataIntegrationConnectionBigDataContent;
