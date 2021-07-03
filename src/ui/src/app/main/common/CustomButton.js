import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';

const BootstrapButton = withStyles({
	root: {
		boxShadow: 'none',
		textTransform: 'none',
		fontSize: 16,
		padding: '6px 12px',
		border: '1px solid',
		lineHeight: 1.5,

		fontFamily: ['Roboto'].join(','),
		'&:hover': {
			boxShadow: 'none'
		},
		'&:active': {
			boxShadow: 'none'
		},
		'&:focus': {
			boxShadow: '0 0 0 0.2rem rgba(0,123,255,.5)'
		},
		'&:disabled': {
			border: '0px' //When disabled don't show border
		}
	}
})(Button);

export default BootstrapButton;
