
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


            <FuseAnimate animation="transition.slideUpIn" delay={200}>

                <div className="flex flex-col md:flex-row sm:p-8 container">


                </div>
            </FuseAnimate>
        </div>
    );
}


export default withReducer('analyticsDashboardApp', reducer)(AnalyticsDashboardApp);
// export default withReducer('analyticsDashboardApp', reducer)(withRouter(connect(mapStateToProps, mapDispatchToProps)(AnalyticsDashboardApp)));
