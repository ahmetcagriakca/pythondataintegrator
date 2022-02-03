
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
import DailyExecutionsWidget from './widgets/DailyExecutionsWidget';
import SourceDataAffectedRowWidget from './widgets/SourceDataAffectedRowWidget';
import MonthlyExecutionsWidget from './widgets/MonthlyExecutionsWidget';
import ExecutionStatuses from './widgets/ExecutionStatuses';


function AnalyticsDashboardApp() {
    const dispatch = useDispatch();
    const widgets = useSelector(selectWidgetsEntities);

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
                                widgets.dailyExecutionsWidget ?
                                    (
                                        <div className="widget flex w-full sm:w-1/4 p-16">
                                            <DailyExecutionsWidget data={widgets.dailyExecutionsWidget} />
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
                    <div className="flex flex-wrap w-full md:w-320">
        
                        {
                            widgets.executionStatuses ?
                                (
                                    <div className="widget w-full p-16">
                                        <ExecutionStatuses data={widgets.executionStatuses} />
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
