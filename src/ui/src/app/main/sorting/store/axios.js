import axios from 'axios';
import { addAuthInterceptors } from '../../../auth/fetchinterceptors';

const instance = axios.create({
	baseURL: window.API_URI
});

addAuthInterceptors(instance);
export default instance;
