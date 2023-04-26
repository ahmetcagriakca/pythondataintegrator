import _ from '@lodash';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import Divider from '@material-ui/core/Divider';
import FormControl from '@material-ui/core/FormControl';
import Icon from '@material-ui/core/Icon';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import { useTheme } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import React, { useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import TableHead from '@material-ui/core/TableHead';
import TableContainer from '@material-ui/core/TableContainer';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
    ellipsis: {
        maxWidth: '80%', // percentage also works
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
    },
});
function ExecutionStatuses({datas}) {
    const classes = useStyles();
    const theme = useTheme();
    const [dataset, setDataset] = useState('today');
    const data = _.merge({}, datas);

    return (
        <Card className="w-full rounded-8 shadow">
            <div className="p-16">
                <Typography className="h1 font-300">Execution Statuses</Typography>
            </div>

            <div className="h-224 relative">
                <Doughnut
                    data={{
                        labels: data.labels,
                        datasets: data.datasets[dataset].map(obj => ({
                            ...obj,
                            borderColor: theme.palette.divider,
                            backgroundColor: [
                                theme.palette.success.dark,
                                theme.palette.error.dark,
                                theme.palette.primary.dark
                            ],
                            hoverBackgroundColor: [
                                theme.palette.success.light,
                                theme.palette.error.light,
                                theme.palette.secondary.light
                            ]
                        }))
                    }}
                    options={data.options}
                />
            </div>

            <div className="p-16 flex flex-row items-center justify-center">
                {data.labels.map((label, index) => (
                    <div key={label} className="px-16 flex flex-col items-center">
                        <Typography className="h4" color="textSecondary">
                            {label}
                        </Typography>
                        <Typography className="h2 font-300 py-8">{data.datasets[dataset][0].data[index]}</Typography>

                        {/* <div className="flex flex-row items-center justify-center">
							{data.datasets[dataset][0].change[index] < 0 && (
								<Icon className="text-18 text-red">arrow_downward</Icon>
							)}

							{data.datasets[dataset][0].change[index] > 0 && (
								<Icon className="text-18 text-green">arrow_upward</Icon>
							)}
							<div className="h5 px-4">{data.datasets[dataset][0].change[index]}</div>
						</div> */}
                    </div>
                ))}
            </div>

            <Divider className="mx-16" />

            <div className="p-16 flex flex-row items-center justify-between">
                <div>
                    <FormControl className="">
                        <Select value={dataset} onChange={ev => setDataset(ev.target.value)}>
                            {Object.keys(data.datasets).map(key => (
                                <MenuItem key={key} value={key}>
                                    {data.datasets[key][0].label}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </div>
                {/* <Button size="small">OVERVIEW</Button> */}
            </div>
            <div className="p-16 px-4 flex flex-row items-center justify-between">
                <Typography className="h1 px-12">Top errors</Typography>
            </div>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: '650' }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell >Name</TableCell>
                            <TableCell align="right" >Count</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {data.datasets[dataset][0]["operationErrorRows"].map((row) => (
                            <React.Fragment>
                                <TableRow
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row">
                                            {row.name}
                                    </TableCell>
                                    <TableCell align="right">{row.count}</TableCell>
                                </TableRow>
                            </React.Fragment>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <div className="p-16 px-4 flex flex-row items-center justify-between">
                <Typography className="h1 px-12">Top Unfinished</Typography>
            </div>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: '650' }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell >Name</TableCell>
                            <TableCell align="right" >Count</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {data.datasets[dataset][0]["operationUnfinishedRows"].map((row) => (
                            <React.Fragment>
                                <TableRow
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row">
                                            {row.name}
                                    </TableCell>
                                    <TableCell align="right">{row.count}</TableCell>
                                </TableRow>
                            </React.Fragment>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

        </Card>
    );
}

export default React.memo(ExecutionStatuses);
