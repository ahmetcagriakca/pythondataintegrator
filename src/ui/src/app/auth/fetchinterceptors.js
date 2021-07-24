import oidcService from 'app/services/oidcService';
import history from '@history';
import { camelizeKeys } from 'humps';

import { toast } from 'react-toastify';

export const addAuthInterceptors = async (axios) => {
  try {
    oidcService.init();
    await oidcService.handleAuthentication();
    if (oidcService.isAuthenticated()) {
      axios.interceptors.request.use((config) => {
        config.headers["Authorization"] =
          "Bearer " + oidcService.getAccessToken();
        config.headers["Content-Type"] = 'application/json';
        config.headers["Access-Control-Allow-Origin"] = "*";
        return config;
      });
    }
  } catch (e) {
    console.log(e);
  }


  axios.interceptors.response.use(
    (response) => {
      if (
        response.data &&
        response.headers['content-type'] === 'application/json'
      ) {
        response.data = camelizeKeys(response.data);
        if (response.data.message && response.data.message !== null && response.data.message !== '') {
          toast.success(response.data.message, { position: toast.POSITION.BOTTOM_RIGHT })
        }
      }

      return response;
    },
    (error) => {
      if (error.response) {
        if (error.response && error.response.status === 401) {
          history.push({
            pathname: window.location.href
          });
          oidcService.login();
        }
        else {
          toast.error(error.response.data.message, { position: toast.POSITION.BOTTOM_RIGHT })
          return Promise.reject(error);
        }
      } else {
        toast.error(error.message, { position: toast.POSITION.BOTTOM_RIGHT })
        console.log(error.stack);
        return Promise.reject(error);
      }
    }
  );
}

