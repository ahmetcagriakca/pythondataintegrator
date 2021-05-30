import FuseNavigation from '@fuse/core/FuseNavigation';
import clsx from 'clsx';
import React from 'react';
import { useSelector } from 'react-redux';
import { selectNavigation } from 'app/store/fuse/navigationSlice';
import reducer from 'app/store';
import withReducer from 'app/store/withReducer';

const recursiveTreeViewer = (typeDescription, data) => {
	let resultArr = [];
	if (isDefined(data) && data[typeDescription] !== undefined) {
		data[typeDescription].forEach(leaf => {
			let deep = getNextSubLeaf(leaf.leafDescription);
			let children = [];
			if (deep !== '' && deep !== undefined && deep !== null) {
				children = recursiveTreeViewer(deep, leaf);
			}

			let currentLeaf = getCurrentLeaf(leaf.leafDescription);
			let tempObj = {
				id: leaf.id,
				title: currentLeaf.rootLevel < 2 && leaf.name ? toTitleCase(leaf.name) : leaf.name,
				type: currentLeaf.type,
				icon: currentLeaf.icon,
				children: children,
			};

			resultArr.push(tempObj);
		});
	}
	return resultArr;
};

const toTitleCase = str => {
	return str.replace(/\w\S*/g, function (txt) {
		return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
	});
};
const MAX_TREE_LEVEL = 3;
const getNextSubLeaf = currentKey => {
	const element = referenceMap[currentKey];
	if (element.rootLevel < MAX_TREE_LEVEL) {
		for (const key in referenceMap) {
			const subElement = referenceMap[key];
			if (subElement.rootLevel - 1 === element.rootLevel) {
				return 'children';
			}
		}
	}

	return '';
};

const getCurrentLeaf = currentKey => {
	const element = referenceMap[currentKey];
	return element;
};

const isDefined = o => {
	return o !== undefined && o !== null;
};

// Tree view deep levels
const referenceMap = {
};

function Navigation(props) {
	const navigation = useSelector(selectNavigation);
	return (
		<FuseNavigation
			className={clsx('navigation', props.className)}
			navigation={navigation}
			layout={props.layout}
			dense={true}
			active={props.active}
		/>
	);
}

Navigation.defaultProps = {
	layout: 'vertical'
};

export default React.memo(withReducer('navigationTree', reducer)(Navigation));
