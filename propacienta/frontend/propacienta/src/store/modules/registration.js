import {
    REGISTRATION_ERROR,
    REGISTRATION_REQUEST,
    REGISTRATION_SUCCESS
} from "../actions/registration";
import request_service from "@/api/HTTP";
const state = {
    registrationStatus: false,
    registrationError: false,
    registrationErrorEmailStatus: false,
    registrationErrorEmailState: '',
    registrationErrorPasswordStatus: false,
    registrationErrorPasswordState: '',



};

const getters = {
    registrationStatus: state => state.registrationStatus,
    registrationError: state => state.registrationError,
    registrationErrorEmailStatus: state => state.registrationErrorEmailStatus,
    registrationErrorEmailState: state => state.registrationErrorEmailState,
    registrationErrorPasswordStatus: state => state.registrationErrorPasswordStatus,
    registrationErrorPasswordState: state => state.registrationErrorPasswordState,

};
const actions = {
    [REGISTRATION_REQUEST]: ({ commit }, user_data) => {
        return new Promise((resolve) => {
            let config = {
                method: "post",
                url: "api/users/",
                data: user_data,
            };
            request_service(
                config,
                function (resp) {
                    console.log(resp.data);
                    commit(REGISTRATION_SUCCESS);
                    resolve(true)
                    //console.log(...resp.headers);
                },
                function (error) {
                    console.log(error.response);
                    commit(REGISTRATION_ERROR, error.response);
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
    [REGISTRATION_SUCCESS]: (state) => {
        state.registrationStatus = true;
        state.registrationError = false;
        state.registrationErrorEmailStatus = false;
        state.registrationErrorEmailState = '';
        state.registrationErrorPasswordStatus = false;
        state.registrationErrorPasswordState = '';
    },
    [REGISTRATION_ERROR]: (state, error_response) => {
        state.registrationStatus = false;
        state.registrationError = true;
        state.registrationErrorEmailState = '';
        if (error_response.data.email != undefined) {
            error_response.data.email.map(item => {
                state.registrationErrorEmailState += ' ' + item
            })
        }
        state.registrationErrorPasswordState = '';
        state.registrationErrorPasswordStatus = false;

        if (error_response.data.password != undefined) {
            error_response.data.password.map(item => {
                state.registrationErrorPasswordState += ' ' + item
            })
        }
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};