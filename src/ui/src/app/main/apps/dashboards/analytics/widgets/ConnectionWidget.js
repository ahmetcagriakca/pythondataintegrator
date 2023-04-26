import React from 'react';
import {withStyles, Card, Icon, Typography} from '@material-ui/core';
import { useTheme } from '@material-ui/core/styles';
import { Line } from 'react-chartjs-2';
import _ from '@lodash';


function ConnectionWidget({datas}) {
	const theme = useTheme();
	const data = _.merge({}, datas);

	return (
		<Card className="w-full rounded-8 shadow">
			<div className="p-16 pb-0 flex flex-row flex-wrap items-end">
				<div className="">
					<Typography className="h3" color="textSecondary">
                    Connections
					</Typography>
					<Typography className="text-56 font-300 leading-none mt-8">{data.data.value}</Typography>
				</div>

				<div className="py-4 text-16 flex flex-row items-center">
					<div className="flex flex-row items-center">
						{data.data.yesterdayDifference > 0 && <Icon className="text-green">trending_up</Icon>}
						{data.data.yesterdayDifference < 0 && <Icon className="text-red">trending_down</Icon>}
						{/* <Typography className="mx-4">{data.data.yesterdayDifference}%</Typography> */}
					</div>
				</div>
			</div>

			<div className="h-96 w-100-p">
                <Line
                    data={{
                        labels  : data.labels,
						datasets: data.datasets.map(obj => ({
							...obj,
							borderColor    : theme.palette.dark,
							backgroundColor: theme.palette.dark
						}))
                    }}
                    options={data.options}
                />
			</div>
		</Card>
	);
}
export default withStyles(null, {withTheme: true})(ConnectionWidget);
