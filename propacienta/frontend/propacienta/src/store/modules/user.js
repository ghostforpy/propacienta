import request_service from "@/api/HTTP";
import {
    CHANGE_USER_ERORR, CHANGE_USER_STATE, CLEAR_USER_STATE, DIALS_ONLINE_TOOGLE, DIALS_TOOGLE, INIT_USER_STATE, TOOGLE_DOC_MODE, USER_REQUEST
} from "../actions/user";
const state = {
    docMode: localStorage.getItem("docMode") == "true",
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
    medicine_card_id: 0,
    doctor_id: 0,
    error: false,
    dials: localStorage.getItem("dials") == "true",
    dialsOnline: false,
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
    medicine_card_id: state => state.medicine_card_id,
    doctor_id: state => state.doctor_id,
    dials: state => state.dials,
    dialsOnline: state => state.dialsOnline,
};
const actions = {
    [USER_REQUEST]: ({ commit }, user_data) => {
        return new Promise((resolve) => {
            let config = {
                method: "patch",
                url: "api/users/me/",
                data: user_data,
            };
            request_service(
                config,
                function (resp) {
                    console.log(resp)
                    commit(CHANGE_USER_STATE, user_data);
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
    [TOOGLE_DOC_MODE]: ({ commit }, docMode) => {
        return new Promise((resolve) => {
            commit(TOOGLE_DOC_MODE, docMode);
            resolve(true)
            //console.log(...resp.headers);
            //console.log(resp.data);
        }
            //
        );
    },
    [DIALS_TOOGLE]: ({ commit }, dials) => {
        return new Promise((resolve) => {
            commit(DIALS_TOOGLE, dials);
            resolve(true)
        }
        );
    },
    [DIALS_ONLINE_TOOGLE]: ({ commit }, dialsStatus) => {
        return new Promise((resolve) => {
            commit(DIALS_ONLINE_TOOGLE, dialsStatus);
            resolve(true)
        }
        );
    },
};
const mutations = {
    [TOOGLE_DOC_MODE]: (state, docMode) => {
        state.docMode = docMode;
        localStorage.setItem("docMode", docMode);
    },
    [DIALS_TOOGLE]: (state, dials) => {
        state.dials = dials;
        localStorage.setItem("dials", dials);
    },
    [DIALS_ONLINE_TOOGLE]: (state, dialsOnline) => {
        state.dialsOnline = dialsOnline;
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
        state.medicine_card_id = user_data.medicine_card;
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
        state.medicine_card_id = 0;
    },
    [CHANGE_USER_STATE]: (state, user_data) => {
        state.error = false;
        state.email = user_data.email;
        state.first_name = user_data.first_name;
        state.last_name = user_data.last_name;
        state.patronymic = user_data.patronymic;
        state.birthday = user_data.birthday;
        state.pacient_phone = user_data.pacient_phone;
        state.doctor_phone = user_data.doctor_phone;
    },
    [CHANGE_USER_ERORR]: (state) => {
        state.error = true;
    },

};

export default {
    state,
    getters,
    actions,
    mutations
};