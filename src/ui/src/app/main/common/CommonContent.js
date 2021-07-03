import React from 'react';
import clsx from 'clsx';

function CommonContentDiv(props) {
	const { content } = props;
	return (
		<div
			className={clsx('flex flex-col flex-1 max-w-2x2 w-full mx-auto px-8 sm:px-32')}
			style={{ padding: '15px 40px 15px 40px' }}
		>
			{content}
		</div>
	);
}

export default CommonContentDiv;
