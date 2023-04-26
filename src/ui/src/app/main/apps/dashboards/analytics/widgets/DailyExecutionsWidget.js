import _ from '@lodash';
import React from 'react';
import { withStyles, Card, Icon, Typography } from '@material-ui/core';
import { Line } from 'react-chartjs-2';

const DailyExecutionsWidget = ({datas, theme}) => {

	const data = _.merge({}, datas);
    const dataWithColors = data.datasets.map(obj => ({
        ...obj,
        borderColor: theme.palette.secondary.main,
        backgroundColor: theme.palette.secondary.main
    }));

    return (
        <Card className="w-full rounded-8 shadow-none border-1">

            <div className="p-16 pb-0 flex flex-row flex-wrap items-end">

                <div className="pr-16">
                    <Typography className="h3" color="textSecondary">Executions</Typography>
                    <Typography className="text-56 font-300 leading-none mt-8">
                        {data.data.value}
                    </Typography>
                </div>
            </div>

            <div className="h-96 w-100-p">
                <Line
                    data={{
                        labels: data.labels,
                        datasets: dataWithColors
                    }}
                    options={data.options}
                />
            </div>
        </Card>
    );
};

export default withStyles(null, { withTheme: true })(DailyExecutionsWidget);
