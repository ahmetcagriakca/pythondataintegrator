
import FuseAnimate from '@fuse/core/FuseAnimate';
import Typography from '@material-ui/core/Typography';
import withReducer from 'app/store/withReducer';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import _ from '@lodash';
import reducer from './store';
import { selectWidgetsEntities, getWidgets } from './store/widgetsSlice';
import {  useTheme } from '@material-ui/core/styles';
import ConnectionWidget from './widgets/ConnectionWidget';
import DataOperationWidget from './widgets/DataOperationWidget';
import DataOperationJobWidget from './widgets/DataOperationJobWidget';
import DailyExecutionsWidget from './widgets/DailyExecutionsWidget';
import SourceDataAffectedRowWidget from './widgets/SourceDataAffectedRowWidget';
import MonthlyExecutionsWidget from './widgets/MonthlyExecutionsWidget';
import ExecutionStatuses from './widgets/ExecutionStatuses';


function AnalyticsDashboardApp() {
    const dispatch = useDispatch();
    const widgets = useSelector(selectWidgetsEntities);
    const theme = useTheme();
    useEffect(() => {
        dispatch(getWidgets());
    }, [dispatch]);

    if (_.isEmpty(widgets)) {
        return null;
    }

    return (
        <div className="w-full">

            <MonthlyExecutionsWidget datas={widgets.monthlyExecutionsWidget} theme={theme} />

            <FuseAnimate animation="transition.slideUpIn" delay={200}>

                <div className="flex flex-col md:flex-row sm:p-8 container">

                <div className="flex flex-1 flex-col min-w-0">
                        <div className="flex flex-col sm:flex sm:flex-row pb-32">
                            {
                                widgets.connectionWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <ConnectionWidget datas={widgets.connectionWidget} theme={theme}/>
                                        </div>
                                    ) : ('')
                            }
                            {
                                widgets.dataOperationWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <DataOperationWidget datas={widgets.dataOperationWidget} theme={theme}/>
                                        </div>
                                    ) : ('')
                            }
                            {
                                widgets.dataOperationJobWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <DataOperationJobWidget datas={widgets.dataOperationJobWidget} theme={theme}/>
                                        </div>
                                    ) : ('')
                            }
                            {
                                widgets.dailyExecutionsWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <DailyExecutionsWidget datas={widgets.dailyExecutionsWidget} theme={theme}/>
                                        </div>
                                    ) : ('')
                            }
                        </div>

                        {
                            widgets.sourceDataAffectedRowWidget ?
                                (
                                    <div className="widget w-full p-16 pb-32">

                                        <SourceDataAffectedRowWidget data={widgets.sourceDataAffectedRowWidget}/>
                                    </div>
                                ) : ('')
                        }

                    </div>
                    <div className="flex flex-wrap w-full md:w-320">

                        {
                            widgets.executionStatuses ?
                                (
                                    <div className="widget w-full p-16">
                                        <ExecutionStatuses datas={widgets.executionStatuses} theme={theme}/>
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
