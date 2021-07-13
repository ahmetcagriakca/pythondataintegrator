
import { makeStyles } from '@material-ui/core/styles';
export const tableStyles = makeStyles(themex => ({
	root: {
		flexGrow: 1
	},
	header: {
		background: `linear-gradient(to left, ${themex.palette.primary.dark} 0%, ${themex.palette.primary.main} 100%)`,
		color: themex.palette.getContrastText(themex.palette.primary.main)
	},
	headerIcon: {
		position: 'absolute',
		top: -64,
		left: 0,
		opacity: 0.04,
		fontSize: 512,
		width: 512,
		height: 512,
		pointerEvents: 'none'
	},
	table: {
		minWidth: 650
	},
	tableRowHeader: {
		height: 70
	},
	tableCell: {
		padding: '0px 16px',
		// backgroundColor: 'gainsboro',
		backgroundColor: '#006565',
		color: 'white',
		// '&:hover': {
		// 	backgroundColor: 'blue !important'
		// }
		hover: {
			'&:hover': {
				backgroundColor: 'green !important'
			}
		}
	}
}));
