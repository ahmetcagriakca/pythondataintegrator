
import FuseAnimate from '@fuse/core/FuseAnimate';
import Typography from '@material-ui/core/Typography';
import withReducer from 'app/store/withReducer';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import _ from '@lodash';
import reducer from './store';
import { selectWidgetsEntities, getWidgets } from './store/widgetsSlice';
import ConnectionWidget from './widgets/ConnectionWidget';
import DataOperationWidget from './widgets/DataOperationWidget';
import DataOperationJobWidget from './widgets/DataOperationJobWidget';
import DataOperationJobExecutionWidget from './widgets/DataOperationJobExecutionWidget';
import SourceDataAffectedRowWidget from './widgets/SourceDataAffectedRowWidget';
import MonthlyExecutionsWidget from './widgets/MonthlyExecutionsWidget';


const analyticsDashboardAppDB = {
    widgets: [
        {
            id: 'monthlyExecutionsWidget',
            chartType: 'line',
            datasets: {
                '2015': [
                    {
                        label: 'Sales',
                        data: [1.9, 3, 3.4, 2.2, 2.9, 3.9, 2.5, 3.8, 4.1, 3.8, 3.2, 2.9],
                        fill: 'start'
                    }
                ],
                '2016': [
                    {
                        label: 'Sales',
                        data: [2.2, 2.9, 3.9, 2.5, 3.8, 3.2, 2.9, 1.9, 3, 3.4, 4.1, 3.8],
                        fill: 'start'
                    }
                ],
                '2017': [
                    {
                        label: 'Sales',
                        data: [3.9, 2.5, 3.8, 4.1, 1.9, 3, 3.8, 3.2, 2.9, 3.4, 2.2, 2.9],
                        fill: 'start'
                    }
                ]
            },
            labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
            options: {
                spanGaps: false,
                legend: {
                    display: false
                },
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 32,
                        left: 32,
                        right: 32
                    }
                },
                elements: {
                    point: {
                        radius: 4,
                        borderWidth: 2,
                        hoverRadius: 4,
                        hoverBorderWidth: 2
                    },
                    line: {
                        tension: 0
                    }
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                display: false,
                                drawBorder: false,
                                tickMarkLength: 18
                            },
                            ticks: {
                                fontColor: '#ffffff'
                            }
                        }
                    ],
                    yAxes: [
                        {
                            display: false,
                            ticks: {
                                min: 1.5,
                                max: 5,
                                stepSize: 0.5
                            }
                        }
                    ]
                },
                plugins: {
                    filler: {
                        propagate: false
                    },
                    xLabelsOnTop: {
                        active: true
                    }
                }
            }
        },
        {
            id: 'connectionWidget',
			conversion: {
				value: 492,
				ofTarget: 13
			},
			chartType: 'bar',
			datasets: [
				{
					label: 'Conversion',
					data: [221, 428, 492, 471, 413, 344, 294]
				}
			],
			labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
			options: {
				spanGaps: false,
				legend: {
					display: false
				},
				maintainAspectRatio: false,
				layout: {
					padding: {
						top: 24,
						left: 16,
						right: 16,
						bottom: 16
					}
				},
				scales: {
					xAxes: [
						{
							display: false
						}
					],
					yAxes: [
						{
							display: false,
							ticks: {
								// min: 100,
								// max: 500
							}
						}
					]
				}
			}
        },
        {
            id: 'dataOperationWidget',
            conversion: {
                value: 25,
                ofTarget: 13
            },
            chartType: 'line',
            datasets: [
                {
                    label: 'Conversion',
                    data: [12, 0, 0, 15, 14, 16, 25]
                }
            ],
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            options: {
                spanGaps: false,
                legend: {
                    display: false
                },
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 24,
                        left: 16,
                        right: 16,
                        bottom: 16
                    }
                },
                scales: {
                    xAxes: [
                        {
                            display: false
                        }
                    ],
                    yAxes: [
                        {
                            display: false,
                            ticks: {
                                // min: 0,
                                // max: 20
                            }
                        }
                    ]
                }
            }
        },
        {
            id: 'dataOperationJobWidget',
            conversion: {
                value: 25,
                ofTarget: 13
            },
            chartType: 'line',
            datasets: [
                {
                    label: 'Conversion',
                    data: [12, 0, 0, 15, 14, 16, 25]
                }
            ],
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            options: {
                spanGaps: false,
                legend: {
                    display: false
                },
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 24,
                        left: 16,
                        right: 16,
                        bottom: 16
                    }
                },
                scales: {
                    xAxes: [
                        {
                            display: false
                        }
                    ],
                    yAxes: [
                        {
                            display: false,
                            ticks: {
                                // min: 0,
                                // max: 20
                            }
                        }
                    ]
                }
            }
        },
        {
            id: 'dataOperationJobExecutionWidget',
            conversion: {
                value: 25,
                ofTarget: 13
            },
            chartType: 'line',
            datasets: [
                {
                    label: 'Conversion',
                    data: [12, 0, 0, 15, 14, 16, 25]
                }
            ],
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            options: {
                spanGaps: false,
                legend: {
                    display: false
                },
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        top: 24,
                        left: 16,
                        right: 16,
                        bottom: 16
                    }
                },
                scales: {
                    xAxes: [
                        {
                            display: false
                        }
                    ],
                    yAxes: [
                        {
                            display: false,
                            ticks: {
                                // min: 0,
                                // max: 20
                            }
                        }
                    ]
                }
            }
        },
        {
            id: 'sourceDataAffectedRowWidget',
            chartType: 'line',
            datasets: {
                yesterday: [
                    {
                        label: 'Source Data Count',
                        data: [190, 300, 340, 220, 290, 390, 250, 380, 410, 380, 320, 290],
                        fill: 'start'
                    },
                    {
                        label: 'Error',
                        data: [2200, 2900, 3900, 2500, 3800, 3200, 2900, 1900, 3000, 3400, 4100, 3800],
                        fill: 'start'
                    }
                ],
                today: [
                    {
                        label: 'Visitors',
                        data: [410, 380, 320, 290, 190, 390, 250, 380, 300, 340, 220, 290],
                        fill: 'start'
                    },
                    {
                        label: 'Page Views',
                        data: [3000, 3400, 4100, 3800, 2200, 3200, 2900, 1900, 2900, 3900, 2500, 3800],
                        fill: 'start'
                    }
                ]
            },
            labels: ['12am', '2am', '4am', '6am', '8am', '10am', '12pm', '2pm', '4pm', '6pm', '8pm', '10pm'],
            options: {
                spanGaps: false,
                legend: {
                    display: false
                },
                maintainAspectRatio: false,
                tooltips: {
                    position: 'nearest',
                    mode: 'index',
                    intersect: false
                },
                layout: {
                    padding: {
                        left: 24,
                        right: 32
                    }
                },
                elements: {
                    point: {
                        radius: 4,
                        borderWidth: 2,
                        hoverRadius: 4,
                        hoverBorderWidth: 2
                    }
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                display: false
                            },
                            ticks: {
                                fontColor: 'rgba(0,0,0,0.54)'
                            }
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                tickMarkLength: 16
                            },
                            ticks: {
                                stepSize: 1000
                            }
                        }
                    ]
                },
                plugins: {
                    filler: {
                        propagate: false
                    }
                }
            }
        },

    ]
};
function AnalyticsDashboardApp() {
    const dispatch = useDispatch();
	const widgets = useSelector(selectWidgetsEntities);
    // const widgets = useSelector((app) => {
    //     return {
    //         connectionWidget: analyticsDashboardAppDB.widgets.filter(w => w.id === 'connectionWidget')[0],
    //         dataOperationWidget: analyticsDashboardAppDB.widgets.filter(w => w.id === 'dataOperationWidget')[0],
    //         dataOperationJobWidget: analyticsDashboardAppDB.widgets.filter(w => w.id === 'dataOperationJobWidget')[0],
    //         dataOperationJobExecutionWidget: analyticsDashboardAppDB.widgets.filter(w => w.id === 'dataOperationJobExecutionWidget')[0],
    //         sourceDataAffectedRowWidget: analyticsDashboardAppDB.widgets.filter(w => w.id === 'sourceDataAffectedRowWidget')[0],
    //         monthlyExecutionsWidget: analyticsDashboardAppDB.widgets.filter(w => w.id === 'monthlyExecutionsWidget')[0],
    //         // widget2: analyticsDashboardAppDB.widgets.filter(w => w.id === 'widget2')[0],
    //         // widget3: analyticsDashboardAppDB.widgets.filter(w => w.id === 'widget3')[0],
    //         // widget4: analyticsDashboardAppDB.widgets.filter(w => w.id === 'widget4')[0],
    //         // widget5: analyticsDashboardAppDB.widgets.filter(w => w.id === 'widget5')[0],
    //         // widget6: analyticsDashboardAppDB.widgets.filter(w => w.id === 'widget6')[0],
    //         // widget7: analyticsDashboardAppDB.widgets.filter(w => w.id === 'widget7')[0],
    //         // widget8: analyticsDashboardAppDB.widgets.filter(w => w.id === 'widget8')[0],
    //         // widget9: analyticsDashboardAppDB.widgets.filter(w => w.id === 'widget9')[0],
    //         // widget2: analyticsDashboardAppDB.widgets[1],
    //         // widget3: analyticsDashboardAppDB.widgets[2],
    //         // widget4: analyticsDashboardAppDB.widgets[3],
    //         // widget5: analyticsDashboardAppDB.widgets[4],
    //         // widget6: analyticsDashboardAppDB.widgets[5],
    //         // widget7: analyticsDashboardAppDB.widgets[6],
    //         // widget8: analyticsDashboardAppDB.widgets[7],
    //         // widget9: analyticsDashboardAppDB.widgets[8],
    //     }
    // });

    useEffect(() => {
        dispatch(getWidgets());
    }, [dispatch]);

    if (_.isEmpty(widgets)) {
        return null;
    }

    return (
        <div className="w-full">

            <MonthlyExecutionsWidget data={widgets.monthlyExecutionsWidget} />

            <FuseAnimate animation="transition.slideUpIn" delay={200}>

                <div className="flex flex-col md:flex-row sm:p-8 container">

                    <div className="flex flex-1 flex-col min-w-0">
                        <div className="flex flex-col sm:flex sm:flex-row pb-32">
                            {
                                widgets.connectionWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <ConnectionWidget data={widgets.connectionWidget} />
                                        </div>
                                    ) : ('')
                            }
                            {
                                widgets.dataOperationWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <DataOperationWidget data={widgets.dataOperationWidget} />
                                        </div>
                                    ) : ('')
                            }
                            {
                                widgets.dataOperationJobWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <DataOperationJobWidget data={widgets.dataOperationJobWidget} />
                                        </div>
                                    ) : ('')
                            }
                            {
                                widgets.dataOperationJobExecutionWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <DataOperationJobExecutionWidget data={widgets.dataOperationJobExecutionWidget} />
                                        </div>
                                    ) : ('')
                            }
                        </div>
                        {
                            widgets.sourceDataAffectedRowWidget ?
                                (
                                    <div className="widget w-full p-16 pb-32">

                                        <SourceDataAffectedRowWidget data={widgets.sourceDataAffectedRowWidget} />
                                    </div>
                                ) : ('')
                        }

                    </div>

                </div>
            </FuseAnimate>
        </div>
    );
}


export default withReducer('analyticsDashboardApp', reducer)(AnalyticsDashboardApp);
// export default withReducer('analyticsDashboardApp', reducer)(withRouter(connect(mapStateToProps, mapDispatchToProps)(AnalyticsDashboardApp)));
