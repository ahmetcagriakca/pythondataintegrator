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
	}
];

export default navigationConfig;
