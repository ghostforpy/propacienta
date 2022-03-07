import {
    TOOGLE_DOC_MODE,
    CHANGE_USER_STATE,
    INIT_USER_STATE,
    CHANGE_USER_ERORR,
    USER_REQUEST,
    CLEAR_USER_STATE
} from "../actions/user";
import request_service from "@/api/HTTP";
const state = {
    docMode: false,
    docModeAvailable: false,
    id: 0,
    email: '',
    first_name: '',
    last_name: '',
    patronymic: '',
    birthday: '',
    pacient_phone: '',
    doctor_phone: '',
    pacient_id: 0,
    doctor_id: 0


};

const getters = {
    docMode: state => state.docMode,
    docModeAvailable: state => state.docModeAvailable,
    id: state => state.id,
    email: state => state.email,
    first_name: state => state.first_name,
    last_name: state => state.last_name,
    patronymic: state => state.patronymic,
    birthday: state => state.birthday,
    pacient_phone: state => state.pacient_phone,
    doctor_phone: state => state.doctor_phone,
    pacient_id: state => state.pacient_id,
    doctor_id: state => state.doctor_id,
};
const actions = {
    [USER_REQUEST]: ({ commit }, user_data) => {
        return new Promise((resolve) => {
            let config = {
                method: "post",
                url: "auth/login/",
                data: user_data,
            };
            request_service(
                config,
                function () {
                    commit(CHANGE_USER_STATE);
                    resolve(true)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                function (error) {
                    commit(CHANGE_USER_ERORR, error.response.status);
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    },
    [CLEAR_USER_STATE]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(CLEAR_USER_STATE);
            resolve(true)
            //console.log(...resp.headers);
            //console.log(resp.data);
        }
            //
        );
    },
};
const mutations = {

    [TOOGLE_DOC_MODE]: (state) => {
        state.docMode = !state.docMode;
    },
    [INIT_USER_STATE]: (state, user_data) => {
        state.docModeAvailable = user_data.doc_mode_available;
        state.id = user_data.id;
        state.email = user_data.email;
        state.first_name = user_data.first_name;
        state.last_name = user_data.last_name;
        state.patronymic = user_data.patronymic;
        state.birthday = user_data.birthday;
        state.pacient_phone = user_data.pacient_phone;
        state.doctor_phone = user_data.doctor_phone;
        state.pacient_id = user_data.pacient_id;
        state.doctor_id = user_data.doctor_id;
    },
    [CLEAR_USER_STATE]: (state) => {
        state.docModeAvailable = false;
        state.id = 0;
        state.email = '';
        state.first_name = '';
        state.last_name = '';
        state.patronymic = '';
        state.birthday = '';
        state.pacient_phone = '';
        state.doctor_phone = '';
        state.pacient_id = 0;
        state.doctor_id = 0;
    },
    [CHANGE_USER_STATE]: (state, user_data) => {
        state.email = user_data.email;
        state.first_name = user_data.first_name;
        state.last_name = user_data.last_name;
        state.patronymic = user_data.patronymic;
        state.birthday = user_data.birthday;
    },

};

export default {
    state,
    getters,
    actions,
    mutations
};