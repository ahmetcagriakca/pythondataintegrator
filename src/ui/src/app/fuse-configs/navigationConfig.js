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
		id: 'sorting',
		title: 'Sorting',
		type: 'group',
		icon: 'Sorting',
		translate: 'SORTING',
		children: [
			{
				id: 'sorting-list',
				title: 'Sorting List',
				type: 'item',
				icon: 'format_list_bulleted',
				translate: 'Sorting_LIST',
				url: '/sorting'
			}
		]
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
	}
];

export default navigationConfig;
