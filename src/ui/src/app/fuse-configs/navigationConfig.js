import i18next from 'i18next';
import en from './navigation-i18n/en';
import tr from './navigation-i18n/tr';

i18next.addResourceBundle('tr', 'navigation', tr);
i18next.addResourceBundle('en', 'navigation', en);

const navigationConfig = [
	{
		id: 'home',
		title: 'Home',
		translate: 'HOME',
		type: 'group',
		icon: 'home',
		url: '/'
	},
	{
		id: 'connections',
		title: 'Connections',
		type: 'group',
		icon: 'connections',
		translate: 'CONNECTIONS',
		children: [
			{
				id: 'connection-list',
				title: 'Connection List',
				type: 'item',
				icon: 'format_list_bulleted',
				translate: 'CONNECTION_LIST',
				url: '/connections'
			}
		]
	},
	{
		id: 'dataoperations',
		title: 'DataOperations',
		type: 'group',
		icon: 'dataoperations',
		translate: 'DATAOPERATIONS',
		children: [
			{
				id: 'data-operation-list',
				title: 'Data Operation List',
				type: 'item',
				icon: 'format_list_bulleted',
				translate: 'DATAOPERATION_LIST',
				url: '/dataoperations'
			}
		]
	},
	
	{
		id: 'dataoperationjobs',
		title: 'DataOperationJobs',
		type: 'group',
		icon: 'dataoperationjobs',
		translate: 'DATAOPERATIONJOBS',
		children: [
			{
				id: 'data-operation--job-list',
				title: 'Data Operation Job List',
				type: 'item',
				icon: 'format_list_bulleted',
				translate: 'DATAOPERATION_JOB_LIST',
				url: '/jobs'
			}
		]
	},
	
	{
		id: 'dataoperationjobexecutions',
		title: 'DataOperationJobExecutions',
		type: 'group',
		icon: 'dataoperationjobexecutions',
		translate: 'DATAOPERATIONJOBEXECUTIONS',
		children: [
			{
				id: 'data-operation--job-execution-list',
				title: 'Data Operation Job Execution List',
				type: 'item',
				icon: 'format_list_bulleted',
				translate: 'DATAOPERATION_JOB_EXECUTION_LIST',
				url: '/job/executions'
			}
		]
	}
];

export default navigationConfig;
