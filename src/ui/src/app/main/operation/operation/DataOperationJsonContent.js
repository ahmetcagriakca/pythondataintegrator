import React, { useEffect } from 'react';
import TextField from '@material-ui/core/TextField';
import JSONPretty from 'react-json-pretty';
import 'react-json-pretty/themes/monikai.css';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

import Tooltip from '@material-ui/core/Tooltip';
import Alert from '@material-ui/lab/Alert';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import { makeStyles } from '@material-ui/core/styles';
import { uuid } from '../../common/utils/Utils';
import { selectConnectionName } from './store/connectionNameSlice';
import { useSelector } from 'react-redux';
import { toast } from 'react-toastify';

const useStyles = makeStyles(theme => ({
	root: {
		"& .MuiTextField-root": {
			margin: theme.spacing(1)
		}
	},
	button: {
		margin: theme.spacing(1),
		"white-space": "nowrap",
	},
	box: {
		display: "flex",
	},
	bottomRightBox: {
		justifyContent: "flex-end",
		alignItems: "flex-end"
	},
	centerBox: {
		justifyContent: "center",
		alignItems: "center"
	},
	topLeftBox: {
		justifyContent: "flex-start",
		alignItems: "flex-start"
	},
	appBar: {
		position: 'relative',
	},
	title: {
		marginLeft: theme.spacing(2),
		flex: 1,
	},
}));
function DataOperationJsonContent(props) {
	const classes = useStyles();
	const { content, setContent, open, setOpen,oldData, oldJsonContent, applyChange } = props;
	const [jsonContent, setJsonContent] = React.useState({});
	const [error, setError] = React.useState(false);
	const [hasError, setHasError] = React.useState(false);
	const [applyTooltip, setApplyTooltip] = React.useState("Apply definition to operation");

	const selectConnectionNames = useSelector(selectConnectionName);
	useEffect(() => {
		try {
			let contentJson = JSON.parse(content)
			setJsonContent(contentJson)
			handleStateChange(false, null)
		}
		catch (error) {
			handleStateChange(true, error.message)
		}
	}, [content])
	const handleContentChange = (event) => {
		let contentValue = event.target.value
		try {
			let contentJson = JSON.parse(contentValue)
			setJsonContent(contentJson)
			handleStateChange(false, null)
		}
		catch (error) {
			handleStateChange(true, error.message)
		}
		finally {
			setContent(contentValue)
		}
	}
	const handleContentBlur = (event) => {
		if (!hasError) {
			setContent(JSON.stringify(jsonContent, null, "\t"))
		}
	}

	const show = (data) => {
		return data
	}

	const handleClose = () => {
		setOpen(false);
	};
	const createOperationFromJson = () => {

		let hasError = false
		if (oldJsonContent.Name && oldJsonContent.Name !== jsonContent.Name) {
			toast.error("Operation name cannot be change. Operation Name:" + oldJsonContent.Name, { position: toast.POSITION.BOTTOM_RIGHT })
			return
		}
		let contacts = []
		for (var i = 0; i < jsonContent.Contacts?.length; i++) {
			contacts = contacts.concat({ id: uuid(), email: jsonContent.Contacts[i].Email })
		}

		let operationIntegrations = []
		for (var j = 0; j < jsonContent.Integrations?.length; j++) {
			let dataOperationIntegration = jsonContent.Integrations[j]
			let operationIntegration = {
				id: uuid(),
				limit: dataOperationIntegration.Limit,
				processCount: dataOperationIntegration.ProcessCount,
				integration: {
					id: uuid(),
					code: dataOperationIntegration.Integration.Code,
					isTargetTruncate: dataOperationIntegration.Integration.IsTargetTruncate,
					comments: dataOperationIntegration.Integration.Comments,
					columns: [
					]
				}
			}
			let columns = []
			if (dataOperationIntegration?.Integration?.SourceConnections && dataOperationIntegration?.Integration?.SourceConnections != null) {
				let sourceConnections = selectConnectionNames.filter(en => en.name == dataOperationIntegration?.Integration?.SourceConnections?.ConnectionName)
				if (sourceConnections?.length > 0) {
					let sourceConnection = null
					let undeletedConnections = sourceConnections.filter(en => en.isDeleted === 0)
					if (undeletedConnections?.length > 0) {
						sourceConnection = undeletedConnections[0]
					}
					else {
						sourceConnection = sourceConnections[0]

					}
					operationIntegration.integration["sourceConnection"] = {
						id: uuid(),
						connection: sourceConnection,
						database: {
							id: uuid(),
							schema: dataOperationIntegration.Integration.SourceConnections.Database.Schema,
							table: dataOperationIntegration.Integration.SourceConnections.Database.Table,
							query: dataOperationIntegration.Integration.SourceConnections.Database.Query
						}
					}
				}
				else {
					toast.error(dataOperationIntegration.Integration.Code + " source connection not found. Connection Name:" + dataOperationIntegration?.Integration?.SourceConnections?.ConnectionName, { position: toast.POSITION.BOTTOM_RIGHT })
				}
				let sourceColumns = dataOperationIntegration?.Integration?.SourceConnections?.Columns?.split(',')
				for (let index = 0; index < sourceColumns.length; index++) {
					const element = sourceColumns[index];
					columns.push({ id: uuid(), sourceColumnName: element, targetColumnName: '' })
				}
			}

			if (dataOperationIntegration?.Integration?.TargetConnections && dataOperationIntegration?.Integration?.TargetConnections != null) {
				let targetConnections = selectConnectionNames.filter(en => en.name == dataOperationIntegration?.Integration?.TargetConnections?.ConnectionName);
				if (targetConnections?.length > 0) {
					let targetConnection = null
					let undeletedConnections = targetConnections.filter(en => en.isDeleted === 0)
					if (undeletedConnections?.length > 0) {
						targetConnection = undeletedConnections[0]
					}
					else {
						targetConnection = targetConnections[0]
					}
					operationIntegration.integration["targetConnection"] = {
						id: uuid(),
						connection: targetConnection,
						database: {
							id: uuid(),
							schema: dataOperationIntegration.Integration.TargetConnections.Database.Schema,
							table: dataOperationIntegration.Integration.TargetConnections.Database.Table,
							query: dataOperationIntegration.Integration.TargetConnections.Database.Query
						}
					}
				}
				else {
					toast.error(dataOperationIntegration.Integration.Code + " target connection not found. Connection Name:" + dataOperationIntegration?.Integration?.TargetConnections?.ConnectionName, { position: toast.POSITION.BOTTOM_RIGHT })
				}
				if (columns?.length > 0) {
					let targetColumns = dataOperationIntegration?.Integration?.TargetConnections?.Columns?.split(',')
					for (let index = 0; index < columns.length; index++) {
						const element = columns[index];
						if (targetColumns?.length > index) {
							element.targetColumnName = targetColumns[index]
						}
					}

				}
			}
			else {
				toast.error(dataOperationIntegration.Integration.Code + " target connection required for integration.", { position: toast.POSITION.BOTTOM_RIGHT })
			}
			if (columns?.length > 0) {
				operationIntegration.integration['columns'] = columns
			}
			operationIntegrations = operationIntegrations.concat(operationIntegration)
		}
		if (!hasError) {
			let operation = {
				id: oldData.id,
				name: jsonContent.Name,
				isDeleted: oldData.Comments,
				definitionId: oldData.definitionId,
				version: oldData.version,
				creationDate: oldData.creationDate,
				contacts: contacts,
				integrations: operationIntegrations
			}
			return operation
		}
		else {
			return null
		}
	}
	const applyAction = () => {
		let operation = createOperationFromJson()
		if (operation) {
			applyChange(operation)
		}
	}

	const handleStateChange = (hasErr, err) => {
		setHasError(hasErr)
		setError(err)
		let tooltipText = hasErr ? "Definition has error" : "Apply definition to operation"
		setApplyTooltip(tooltipText)
	}

	return (

		<Dialog fullScreen
			fullWidth={true}
			maxWidth={"sm"}
			open={open}
			on
			onClose={handleClose}
			aria-labelledby="max-width-dialog-title"
		>
			<AppBar className={classes.appBar}>
				<Toolbar>
					<IconButton edge="start" color="inherit" onClick={handleClose} aria-label="close">
						<Icon>close</Icon>
					</IconButton>
				</Toolbar>
			</AppBar>
			<DialogTitle id="max-width-dialog-title"  >
				<Grid item xs={12}>
					<Box >
						Definition
					</Box>
				</Grid>
				{
					hasError ?
						(
							<Grid item xs={12}>
								<Box >

									<Alert severity="error">
										{error}
									</Alert>
								</Box>
							</Grid>
						) : ('')
				}
			</DialogTitle>
			<DialogContent>
				<Box style={{ width: '100%', padding: '10px 0 0 0' }}>

					<div style={{ maxHeight: "100%" }}>
						<Box>
							<Grid container spacing={3}>
								<Grid item xs={6}>
									<TextField
										placeholder="Definition Json"
										multiline
										minrows={16}
										maxrows={16}
										fullWidth={true}
										variant="outlined"
										value={content}
										onChange={event => handleContentChange(event)}
										onBlur={event => handleContentBlur(event)}
									/>
								</Grid>
								<Grid item xs={6}>
									<JSONPretty id="prettyDefinitionJson" data={show(jsonContent)}></JSONPretty>
								</Grid>
							</Grid>
						</Box>

					</div>
				</Box>
			</DialogContent>
			<DialogActions>
				<Tooltip title={applyTooltip}>
					<span>
						<Button
							disabled={hasError}
							onClick={applyAction}
							variant="contained"
							color="secondary"
							size="large">
							Apply
						</Button>
					</span>
				</Tooltip>
				<Button onClick={handleClose} color="secondary">
					Close
				</Button>
			</DialogActions>
		</Dialog>
	)
}

export default DataOperationJsonContent;
