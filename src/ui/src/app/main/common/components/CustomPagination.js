import Pagination from '@material-ui/lab/Pagination';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import Grid from '@material-ui/core/Grid';

import React from 'react';

class CustomPagination extends React.Component {

	render() {
		const {
			rowsPerPage,
			page,
			totalCount,
			handleChangePage,
			handleChangeRowsPerPage,
		} = this.props;
		let count = totalCount === 0 ? parseInt(totalCount / rowsPerPage) : parseInt((totalCount % rowsPerPage) === 0 ? (totalCount / rowsPerPage) : ((totalCount / rowsPerPage) + 1))
		let start = rowsPerPage * (page - 1)
		let end = (rowsPerPage * (page)) > totalCount ? totalCount : rowsPerPage * (page)
		return (

			<div style={{ height: 60 }}>
				<Grid container spacing={3}>
					<Grid item xs={4}>
					</Grid>
					<Grid item xs={5}>
						<div style={{ padding: 5 }}>
							<Pagination
								shape="rounded"
								count={count}
								showFirstButton
								showLastButton
								page={page}
								onChange={handleChangePage}
								style={{ fontSize: 24 }}
							/>
						</div>
					</Grid>
					<Grid item xs={3}>
						<div style={{ float: 'right', padding: 5 }}>
							<label><b>Rows Per Page:</b></label>
							<Select
								style={{ padding: 5 }}
								labelId="rowsPerPage"
								id="rowsPerPage"
								value={rowsPerPage}
								onChange={handleChangeRowsPerPage}
							>
								<MenuItem value={5}>5</MenuItem>
								<MenuItem value={10}>10</MenuItem>
								<MenuItem value={25}>25</MenuItem>
								<MenuItem value={50}>50</MenuItem>
							</Select>
							<label><b>{start}-{end} of {totalCount}</b></label>
						</div>
					</Grid>
				</Grid>
			</div>
		);
	}
}


export default CustomPagination;