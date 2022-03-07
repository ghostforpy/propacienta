import {
    REGISTRATION_ERROR,
    REGISTRATION_REQUEST,
    REGISTRATION_SUCCESS,
    ACTIVATE_REGISTRATION_ERROR,
    ACTIVATE_REGISTRATION_SUCCESS,
    ACTIVATE_REGISTRATION_REQUEST,
    ACTIVATE_ON_LOAD
} from "../actions/registration";
import request_service from "@/api/HTTP";
const state = {
    registrationStatus: false,
    registrationError: false,
    registrationErrorState: '',
    registrationErrorEmailStatus: false,
    registrationErrorEmailState: '',
    registrationErrorPasswordStatus: false,
    registrationErrorPasswordState: '',
    activateRegistrationStatus: false,
    activateRegistrationError: false,
    activateRegistrationErrorResponce: '',
    registrationErrorPhoneStatus: false,
    registrationErrorPhoneState: '',
    activateOnLoad: false


};

const getters = {
    registrationStatus: state => state.registrationStatus,
    registrationError: state => state.registrationError,
    registrationErrorState: state => state.registrationErrorState,
    registrationErrorEmailStatus: state => state.registrationErrorEmailStatus,
    registrationErrorEmailState: state => state.registrationErrorEmailState,
    registrationErrorPasswordStatus: state => state.registrationErrorPasswordStatus,
    registrationErrorPasswordState: state => state.registrationErrorPasswordState,
    activateRegistrationStatus: state => state.activateRegistrationStatus,
    activateRegistrationError: state => state.activateRegistrationError,
    registrationErrorPhoneStatus: state => state.registrationErrorPhoneStatus,
    registrationErrorPhoneState: state => state.registrationErrorPhoneState,
    activateOnLoad: state => state.activateOnLoad,

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
                function () {
                    // function (resp) {
                    // console.log(resp.data);
                    commit(REGISTRATION_SUCCESS);
                    resolve(true)
                    //console.log(...resp.headers);
                },
                function (error) {
                    // console.log(error.response);
                    commit(REGISTRATION_ERROR, error.response);
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    },
    [ACTIVATE_REGISTRATION_REQUEST]: ({ commit }, data) => {
        return new Promise((resolve) => {
            let config = {
                method: "post",
                url: "api/users/activation/",
                data: data,
            };
            request_service(
                config,
                function () {
                    commit(ACTIVATE_REGISTRATION_SUCCESS);
                    resolve(true)
                },
                function (error) {
                    commit(ACTIVATE_REGISTRATION_ERROR, error.response);
                    resolve(false)
                },
            );
        });
    },
    [ACTIVATE_ON_LOAD]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(ACTIVATE_ON_LOAD);
            resolve(true)
        });
    },
};
const mutations = {
    [REGISTRATION_SUCCESS]: (state) => {
        state.registrationStatus = true;
        state.registrationError = false;
        state.registrationErrorState = '';
        state.registrationErrorEmailStatus = false;
        state.registrationErrorEmailState = '';
        state.registrationErrorPasswordStatus = false;
        state.registrationErrorPasswordState = '';
        state.registrationErrorPhoneStatus = false;
        state.registrationErrorPhoneState = '';
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
        state.registrationErrorPhoneStatus = true;
        state.registrationErrorPhoneState = '';
        if (error_response.data.phone_doctor != undefined) {
            error_response.data.phone_doctor.map(item => {
                state.registrationErrorPhoneState += ' ' + item
            })
        }
        if (error_response.data.phone_pacient != undefined) {
            error_response.data.phone_pacient.map(item => {
                state.registrationErrorPhoneState += ' ' + item
            })
        }
        state.registrationErrorState = '';
        if (error_response.data.non_field_errors != undefined) {
            error_response.data.non_field_errors.map(item => {
                state.registrationErrorState += ' ' + item
            })
        }

    },
    [ACTIVATE_REGISTRATION_SUCCESS]: (state) => {
        state.activateRegistrationStatus = true;
        state.activateRegistrationError = false;
        state.activateOnLoad = false;
    },
    [ACTIVATE_REGISTRATION_ERROR]: (state, error_response) => {
        state.activateRegistrationStatus = false;
        state.activateRegistrationError = true;
        state.activateRegistrationErrorResponce = error_response;
        state.activateOnLoad = false;
    },
    [ACTIVATE_ON_LOAD]: (state) => {
        state.activateOnLoad = true;
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};