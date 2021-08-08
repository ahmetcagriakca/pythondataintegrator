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
		type: 'item',
		icon: 'house',
		url  : '/apps/dashboards/analytics'
	},
	{
		id: 'connections',
		title: 'Connections',
		type: 'group',
		icon: 'https',
		translate: 'CONNECTIONS',
		children: [
			{
				id: 'connection-list',
				title: 'Connection List',
				type: 'item',
				icon: 'https',
				translate: 'CONNECTION_LIST',
				url: '/connections',
			}
		]
	},
	{
		id: 'dataoperations',
		title: 'DataOperations',
		type: 'group',
		icon: 'library_books',
		translate: 'DATAOPERATIONS',
		children: [
			{
				id: 'data-operation-list',
				title: 'Data Operation List',
				type: 'item',
				icon: 'library_books',
				translate: 'DATAOPERATION_LIST',
				url: '/operations'
			},
			{
				id: 'data-operation--job-list',
				title: 'Data Operation Job List',
				type: 'item',
				icon: 'repeat',
				translate: 'DATAOPERATION_JOB_LIST',
				url: '/jobs'
			},
			
			{
				id: 'data-operation--job-execution-list',
				title: 'Data Operation Job Execution List',
				type: 'item',
				icon: 'play_arrow',
				translate: 'DATAOPERATION_JOB_EXECUTION_LIST',
				url: '/job/executions'
			}
		]
	},
	
];

export default navigationConfig;
