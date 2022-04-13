import request_service from "@/api/HTTP";
import {
    AUTH_ERROR, AUTH_LOGOUT,
    AUTH_PING, AUTH_REQUEST, AUTH_SUCCESS, LOGOUT_ERROR
} from "../actions/auth";
import { CLEAR_USER_STATE, INIT_USER_STATE } from "../actions/user";
const state = {
    isAuthenticated: '',
    authError: false,
    authErrorStatus: 0,
    logoutError: false,
    logoutErrorStatus: 0,

};

const getters = {
    isAuthenticated: state => state.isAuthenticated,
    authError: state => state.authError,
    authErrorStatus: state => state.authErrorStatus,
    logoutError: state => state.logoutError,
    logoutErrorStatus: state => state.logoutErrorStatus,
};
const actions = {
    [AUTH_PING]: ({ commit }) => {
        return new Promise((resolve) => {
            let config = {
                method: "get",
                url: "api/users/me/",
            };
            request_service(
                config,
                function (resp) {
                    commit(AUTH_SUCCESS);
                    // console.log('ping sucsess')
                    commit(INIT_USER_STATE, resp.data)
                    resolve(true)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                function () {
                    commit(AUTH_ERROR);
                    // console.log("auth ping err")
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
            return false
        })
    },

    [AUTH_REQUEST]: ({ commit }, user_data) => {
        return new Promise((resolve) => {
            let config = {
                method: "post",
                url: "auth/login/",
                data: user_data,
            };
            request_service(
                config,
                function (resp) {
                    commit(AUTH_SUCCESS);
                    commit(INIT_USER_STATE, resp.data)
                    resolve(true)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                function (error) {
                    commit(AUTH_ERROR, error.response.status);
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    },
    [AUTH_LOGOUT]: ({ commit }) => {
        return new Promise(resolve => {
            let config = {
                method: "post",
                url: "auth/logout/",
            };
            request_service(
                config,
                function () {
                    commit(AUTH_LOGOUT);
                    commit(CLEAR_USER_STATE);
                    resolve(true)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                function (error) {
                    commit(LOGOUT_ERROR, error.response.status);
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    }
};
const mutations = {

    [AUTH_SUCCESS]: (state) => {
        state.isAuthenticated = true;
        state.authError = false;
        state.authErrorStatus = 0
    },
    [AUTH_ERROR]: (state, err) => {
        state.authErrorStatus = err;
        state.authError = true;
        state.isAuthenticated = false;
    },
    [AUTH_LOGOUT]: state => {
        state.isAuthenticated = false;
        state.logoutError = false;
        state.logoutErrorStatus = 0
    },
    [LOGOUT_ERROR]: (state, err) => {
        state.logoutErrorStatus = err;
        state.logoutError = true;
        //state.isAuthenticated = false;
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};