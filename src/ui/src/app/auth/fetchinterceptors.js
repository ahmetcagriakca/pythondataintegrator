import oidcService from 'app/services/oidcService';
import history from '@history';
import { camelizeKeys } from 'humps';

export const addAuthInterceptors = async (axios) =>{
    try{
        oidcService.init();
        await oidcService.handleAuthentication();
        if(oidcService.isAuthenticated()){
            axios.interceptors.request.use((config) => {
                config.headers["Authorization"] =
                  "Bearer " + oidcService.getAccessToken();
                config.headers["Content-Type"] = 'application/json';
                config.headers["Access-Control-Allow-Origin"] = "*";
              return config;
            });
        }
    }catch(e){
        console.log(e);
    }
    

    axios.interceptors.response.use(
      (response) => {
        if (
          response.data &&
          response.headers['content-type'] === 'application/json'
        ) {
          response.data = camelizeKeys(response.data);
        }
        return response;
      },
      (error) => {
        if (401 === error.response.status) {
            history.push({
                pathname: window.location.href
            });
            oidcService.login();
        } else {
          return Promise.reject(error);
        }
      }
    );
}

