import request_service from "@/api/HTTP";
import {
    ADD_CHAT,
    ADD_MESSAGE,
    ADD_MESSAGES,
    GET_CHATS,
    GET_MESSAGES,
    // OPEN_CHAT,
    SET_ACTIVE_CHAT,
    SET_CHATS,
    SET_MESSAGES,
    SET_MESSAGES_PAGE,
    SET_NEW_MESSAGES,
    SET_SELF_ID,
    TOOGLE_CHATS_VISIBLE,
    UNSET_NEW_MESSAGES
} from "../actions/chats";

const state = {
    activeChatId: 0,
    listChatsVisible: true,
    chats: new Array(), // Array[chat_objects]
    messages: new Map(), // Map[chat_id]:Array[message_objects]
    messagesPages: new Map(),// Map[chat_id]:Array[next_page]
    activeChatMessagesNextPage: 1,
    activeChatMessages: new Array(), // Array[message_objects]
    activeChatMembers: new Array(),
    activeChatTitle: "",
    selfId: 0,
    activeChatOpponentId: 0,
    chatsVisible: false,
    newMessages: false,
};

const getters = {
    activeChatId: state => state.activeChatId,
    listChatsVisible: state => state.listChatsVisible,
    chats: state => state.chats,
    messages: state => state.messages,
    messagesPages: state => state.messagesPages,
    activeChatMessagesNextPage: state => state.activeChatMessagesNextPage,
    activeChatMessages: state => state.activeChatMessages,
    activeChatMembers: state => state.activeChatMembers,
    activeChatTitle: state => state.activeChatTitle,
    selfId: state => state.selfId,
    activeChatOpponentId: state => state.activeChatOpponentId,
    chatsVisible: state => state.chatsVisible,
    newMessages: state => state.newMessages,
};
const actions = {
    [GET_CHATS]: ({ commit }) => {
        return new Promise((resolve) => {
            let config = {
                method: "get",
                url: "api/dialogs/",
            };
            request_service(
                config,
                function (resp) {
                    // console.log(resp)
                    commit(SET_CHATS, resp.data);
                    resolve(true)
                },
                // function (error) {
                function () {
                    // commit(CHANGE_USER_ERORR, error.response.status);
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    },
    [SET_ACTIVE_CHAT]: ({ commit, state, dispatch }, chatId) => {
        return new Promise((resolve) => {
            const chat = state.chats.find(chat => chat.id === chatId)
            if (!chat.opened) {
                dispatch('GET_MESSAGES', chatId).then(() => {
                    commit(SET_ACTIVE_CHAT, { chatId: chatId, chat: chat });
                })
            } else {
                commit(SET_ACTIVE_CHAT, { chatId: chatId, chat: chat });
            }
            resolve(true)
            //console.log(...resp.headers);
            //console.log(resp.data);
        }
            //
        );
    },
    // [OPEN_CHAT]: ({ commit, state, dispatch }, chatId) => {
    //     return new Promise((resolve) => {
    //         commit(SET_ACTIVE_CHAT, chatId);
    //         resolve(true)
    //         //console.log(...resp.headers);
    //         //console.log(resp.data);
    //     }
    //         //
    //     );
    // },
    [ADD_CHAT]: ({ commit }, chat) => {
        return new Promise((resolve) => {
            commit(ADD_CHAT, chat);
            resolve(true)
            //console.log(...resp.headers);
            //console.log(resp.data);
        }
            //
        );
    },
    [GET_MESSAGES]: ({ commit, state }, chatId) => {
        return new Promise((resolve) => {
            var page = 0
            if (state.messagesPages.has(chatId)) {
                page = state.messagesPages.get(chatId)
            } else {
                page = 1
            }
            if (page == null) {
                return
            }
            let config = {
                method: "get",
                url: "api/dialog-messages/",
                params: {
                    dialog: chatId,
                    page: page
                },
            };
            request_service(
                config,
                function (resp) {
                    // console.log(resp, page)
                    if (page == 1) {
                        // console.log(resp.data.results)
                        commit(SET_MESSAGES, { chatId: chatId, messages: resp.data.results });

                    } else {
                        commit(ADD_MESSAGES, { chatId: chatId, messages: resp.data.results });
                    }
                    var nextPage = null;
                    if (resp.data.next != null) {
                        let nextUrl = new URL(resp.data.next);
                        nextPage = nextUrl.searchParams.get("page")
                    }
                    commit(SET_MESSAGES_PAGE, { chatId: chatId, nextPage: nextPage })
                    resolve(true)
                },
                function (error) {
                    // function () {
                    console.log(error)
                    // commit(CHANGE_USER_ERORR, error.response.status);
                    resolve(false)
                    //console.log(...resp.headers);
                    //console.log(resp.data);
                },
                //
            );
        });
    },
    [ADD_MESSAGE]: ({ commit }, chatId, message) => {
        return new Promise((resolve) => {
            commit(ADD_MESSAGE, chatId, message);
            resolve(true)
        }
        );
    },
    [SET_SELF_ID]: ({ commit }, selfId) => {
        return new Promise((resolve) => {
            commit(SET_SELF_ID, selfId);
            resolve(true)
        }
        );
    },
    [TOOGLE_CHATS_VISIBLE]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(TOOGLE_CHATS_VISIBLE);
            resolve(true)
        }
        );
    },
    [SET_NEW_MESSAGES]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(SET_NEW_MESSAGES);
            resolve(true)
        }
        );
    },
    [UNSET_NEW_MESSAGES]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(UNSET_NEW_MESSAGES);
            resolve(true)
        }
        );
    },
};
const mutations = {
    [SET_ACTIVE_CHAT]: (state, { chatId, chat }) => {
        state.activeChatId = chatId;
        state.activeChatMessages = state.messages.get(chatId);
        state.activeChatMessagesNextPage = state.messagesPages.get(chatId) == undefined ? 1 : state.messagesPages.get(chatId)
        // const chat = state.chats.find(chat => chat.id === chatId)
        state.activeChatMembers = chat.members;
        state.activeChatTitle = chat.title;
        if (!chat.opened) {
            var chats = state.chats
            chats.forEach(item => {
                if (item.id == chatId) {
                    item.opened = true
                }
            })
            state.chats = chats
        }
    },
    [SET_CHATS]: (state, chats) => {
        chats.forEach(item => {
            item.title = item.members.find(member => member.id != state.selfId).fio
            item.opened = false
            return item
        });
        state.chats = chats;
    },
    [ADD_CHAT]: (state, chat) => {
        chat.title = chat.members.find(member => member.id != state.selfId).fio
        chat.opened = false;
        state.chats.unshift(chat);
    },
    [SET_MESSAGES]: (state, { chatId, messages }) => {
        var msgs = state.messages
        msgs.set(chatId, messages.reverse())
        state.messages = msgs

    },
    [ADD_MESSAGES]: (state, { chatId, messages }) => {
        let msgs = state.messages.get(chatId)
        msgs.unshift(...messages.reverse()); // проверить
        state.messages.set(chatId, msgs)
    },
    [ADD_MESSAGE]: (state, { chatId, message }) => {
        let msgs = state.messages.get(chatId)
        msgs.unshift(message);
        state.messages.set(chatId, msgs)
    },
    [SET_MESSAGES_PAGE]: (state, { chatId, nextPage }) => {
        state.messagesPages.set(chatId, nextPage)
    },
    [SET_SELF_ID]: (state, selfId) => {
        state.selfId = selfId
    },
    [TOOGLE_CHATS_VISIBLE]: (state) => {
        state.chatsVisible = !state.chatsVisible
    },
    [SET_NEW_MESSAGES]: (state) => {
        state.newMessages = true
    },
    [UNSET_NEW_MESSAGES]: (state) => {
        state.newMessages = false
    },

};

export default {
    state,
    getters,
    actions,
    mutations
};