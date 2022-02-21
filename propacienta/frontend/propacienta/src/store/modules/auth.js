import {
    AUTH_REQUEST,
    AUTH_ERROR,
    AUTH_SUCCESS,
    AUTH_LOGOUT,
    AUTH_PING
} from "../actions/auth";
import request_service from "@/api/HTTP";
const state = {
    isAuthenticated: false,
    authError: false,
};

const getters = {
    isAuthenticated: state => state.isAuthenticated,
    authError: state => state.authError,
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
                    console.log('ping sucsess')
                    resolve(resp)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                function () {
                    commit(AUTH_ERROR);
                    console.log("auth ping err")
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        })
    },

    [AUTH_REQUEST]: ({ commit }, user_data) => {
        return new Promise((resolve) => {
            //commit(AUTH_REQUEST);
            //let user_data = {
            //    email: this.email,
            //    password: this.password,
            //};
            let config = {
                method: "post",
                url: "auth-token/",
                data: user_data,
            };
            request_service(
                config,
                function (resp) {
                    commit(AUTH_SUCCESS);
                    resolve(resp)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                function () {
                    commit(AUTH_ERROR);
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    },
    [AUTH_LOGOUT]: ({ commit }) => {
        return new Promise(resolve => {
            commit(AUTH_LOGOUT);
            localStorage.removeItem("user-token");
            resolve();
        });
    }
};
const mutations = {
    //[AUTH_REQUEST]: state => {
    //    state.status = "loading";
    //},
    [AUTH_SUCCESS]: (state) => {
        state.isAuthenticated = true;
        state.authError = false;
        //state.token = resp.token;
        //state.hasLoadedOnce = true;
    },
    [AUTH_ERROR]: state => {
        state.authError = true;
        state.isAuthenticated = false;
    },
    [AUTH_LOGOUT]: state => {
        state.isAuthenticated = false;
        state.authError = false;
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};