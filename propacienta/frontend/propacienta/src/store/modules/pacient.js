import {
    MEDICINECARD_COMMON_GET,
    MEDICINECARD_COMMON_GET_SUCCESS,
    INIT_PACIENT_STATE,
    PACIENT_ERROR,
    MEDICINECARD_COMMON_PATCH_SUCCESS,
    MEDICINECARD_COMMON_PATCH_REQUEST,
    CLEAR_PACIENT_STATE
} from "../actions/pacient";
import request_service from "@/api/HTTP";
const state = {
    pacientId: 0,
    medicineCardId: 0,
    commondataResp: {},
    error: false
};

const getters = {
    pacientId: state => state.pacientId,
    medicineCardId: state => state.medicineCardId,
    commondataResp: state => state.commondataResp,
};
const actions = {
    [INIT_PACIENT_STATE]: ({ commit }, data) => {
        return new Promise((resolve) => {
            commit(INIT_PACIENT_STATE, data);
            resolve(true)
        });
    },
    [MEDICINECARD_COMMON_GET]: ({ commit, state }) => {
        return new Promise((resolve) => {
            let config = {
                method: "get",
                url: `api/medicine-cards/${state.medicineCardId}/`,
            };
            request_service(
                config,
                function (resp) {
                    // console.log(resp)
                    commit(MEDICINECARD_COMMON_GET_SUCCESS, resp.data);
                    resolve(true)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                function (error) {
                    commit(PACIENT_ERROR, error.response.status);
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    },
    [MEDICINECARD_COMMON_PATCH_REQUEST]: ({ commit, state }, user_data) => {
        return new Promise((resolve) => {
            let config = {
                method: "patch",
                url: `api/medicine-cards/${state.medicineCardId}/`,
                data: user_data,
            };
            request_service(
                config,
                function () {
                    // console.log(resp)
                    commit(MEDICINECARD_COMMON_PATCH_SUCCESS);
                    resolve(true)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                function (error) {
                    commit(PACIENT_ERROR, error.response.status);
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    },
    [CLEAR_PACIENT_STATE]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(CLEAR_PACIENT_STATE);
            resolve(true)
            //console.log(...resp.headers);
            //console.log(resp.data);
        }
            //
        );
    },
};
const mutations = {
    [INIT_PACIENT_STATE]: (state, data) => {
        state.pacientId = data.pacient;
        state.medicineCardId = data.medicine_card;
    },
    [MEDICINECARD_COMMON_PATCH_SUCCESS]: (state) => {
        state.error = false;
    },
    [MEDICINECARD_COMMON_GET_SUCCESS]: (state, data) => {
        state.error = false;
        state.commondataResp = data;
    },
    [CLEAR_PACIENT_STATE]: (state) => {
        state.commondataResp = "";
        state.pacientID = 0;
    },
    // [CHANGE_USER_STATE]: (state, user_data) => {
    //     state.error = false;
    //     state.email = user_data.email;
    //     state.first_name = user_data.first_name;
    //     state.last_name = user_data.last_name;
    //     state.patronymic = user_data.patronymic;
    //     state.birthday = user_data.birthday;
    //     state.pacient_phone = user_data.pacient_phone;
    //     state.doctor_phone = user_data.doctor_phone;
    // },
    [PACIENT_ERROR]: (state) => {
        state.error = true;
    },

};

export default {
    state,
    getters,
    actions,
    mutations
};