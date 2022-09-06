import request_service from "@/api/HTTP";
import {
    ADD_CHAT,
    ADD_MESSAGE,
    ADD_MESSAGES,
    GET_CHATS,
    GET_MESSAGES, HANDLE_READ_MESSAGES, HANDLE_SERVICE_MESSAGE,
    HANDLE_USER_STATUS_MESSAGE, OPEN_CHAT, SET_ACTIVE_CHAT,
    SET_CHATS, SET_CHATS_UNVISIBLE, SET_CHATS_VISIBLE, SET_CHAT_SOCKET, SET_CHAT_WINDOW_CLOSE, SET_CHAT_WINDOW_OPEN, SET_MESSAGES,
    SET_MESSAGES_PAGE, SET_NEW_MESSAGES, SET_READ_MSGS_NOTIFIER, TOOGLE_CHATS_VISIBLE,
    UNSET_NEW_MESSAGES
} from "../actions/chats";

function check_read_msgs(state, chatId, msgs) {
    let messages_ids = []
    // unread_messages.forEach(msg => {
    //     msg.read_by_the_user = true
    //     messages_ids.push(msg.id)
    // })
    //sender_id
    var all_msgs = state.messages
    all_msgs.set(chatId, msgs.map(msg => {
        if (!msg.read_by_the_user && msg.sender == state.activeChatOpponentId) {
            msg.read_by_the_user = true
            messages_ids.push(msg.id)
        }
        return msg
    }))
    // state.messages = all_msgs
    state.readMsgsNotifier(messages_ids, chatId, state.activeChatOpponentId)
    return all_msgs
}

const state = {
    chatSocket: null,
    activeChatId: 0,
    listChatsVisible: true,
    chatWindowIsOpen: false,
    chats: new Array(), // Array[chat_objects]
    messages: new Map(), // Map[chat_id]:Array[message_objects]
    messagesPages: new Map(),// Map[chat_id]:Array[next_page]
    activeChatMessagesNextPage: 1,
    activeChatMessages: new Array(), // Array[message_objects]
    activeChatMembers: new Array(),
    activeChatTitle: "",
    readMsgsNotifier: null,
    // activeChatIsOpen: false,
    // selfId: 0,
    activeChatOpponentId: 0,
    chatsVisible: true,
    newMessages: false,
};

const getters = {
    selfId(state, getters, rootState, rootGetters) {
        return rootGetters.id
    },
    chatSocket: state => state.chatSocket,
    activeChatId: state => state.activeChatId,
    listChatsVisible: state => state.listChatsVisible,
    chatWindowIsOpen: state => state.chatWindowIsOpen,
    chats: state => state.chats,
    messages: state => state.messages,
    messagesPages: state => state.messagesPages,
    activeChatMessagesNextPage: state => state.activeChatMessagesNextPage,
    activeChatMessages: state => state.activeChatMessages,
    activeChatMembers: state => state.activeChatMembers,
    activeChatTitle: state => state.activeChatTitle,
    activeChatIsOpen: state => state.activeChatIsOpen,
    // selfId: state => state.selfId,
    activeChatOpponentId: state => state.activeChatOpponentId,
    chatsVisible: state => state.chatsVisible,
    newMessages: state => state.newMessages,
};
const actions = {
    [GET_CHATS]: ({ commit, getters }) => {
        return new Promise((resolve) => {
            let config = {
                method: "get",
                url: "api/dialogs/",
            };
            request_service(
                config,
                function (resp) {
                    // console.log(resp)
                    setTimeout(() => {
                        commit(SET_CHATS, { chats: resp.data, selfId: getters.selfId });
                        resolve(true)
                    }, 500);

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
    [SET_ACTIVE_CHAT]: ({ commit, state, dispatch, getters }, { chatId }) => {
        return new Promise((resolve) => {
            const chat = state.chats.find(chat => chat.id === chatId)
            if (!chat.opened) {
                dispatch('GET_MESSAGES', chatId).then(() => {
                    commit(SET_ACTIVE_CHAT, { chatId: chatId, chat: chat, selfId: getters.selfId });
                })
            } else {
                commit(SET_ACTIVE_CHAT, { chatId: chatId, chat: chat, selfId: getters.selfId });
            }
            resolve(true)
            //console.log(...resp.headers);
            //console.log(resp.data);
        }
            //
        );
    },
    // [OPEN_CHAT]: ({ commit, state, dispatch }, { opponentId }) => {
    [OPEN_CHAT]: ({ commit, state, dispatch, getters }, { opponentType, opponentId }) => {
        return new Promise((resolve) => {
            const chat = state.chats.find(chat => {
                // let opponent = chat.members.find(member => member.id != state.selfId)
                let opponent = chat.members.find(member => member.id != getters.selfId)
                return opponentType == "doctor" ? opponent.doctor_id === opponentId : opponent.pacient_id === opponentId
            })
            if (chat != undefined) {
                dispatch(SET_ACTIVE_CHAT, { chatId: chat.id })
                dispatch(SET_CHATS_UNVISIBLE);
                resolve(true)
            } else {
                // создать диалог
                let form = new FormData();
                form.append("opponent_id", opponentId);
                form.append("opponent_type", opponentType);
                let config = {
                    method: "post",
                    url: "api/dialogs/",
                    data: form,
                };
                if (opponentType == "pacient") {
                    config.headers = {
                        IsDoctor: true,
                    }
                }
                request_service(
                    config,
                    function (resp) {
                        const newChat = resp.data
                        commit(ADD_CHAT, newChat)
                        dispatch(SET_ACTIVE_CHAT, { chatId: newChat.id })
                        dispatch(SET_CHATS_UNVISIBLE);
                        resolve(true)
                    },
                    function (error) {
                        console.log(error);
                        resolve(false)
                    }
                );

            }

        }
        );
    },
    [HANDLE_SERVICE_MESSAGE]: ({ commit }, { chatId, serviceType, messageId }) => {
        return new Promise((resolve) => {
            commit(HANDLE_SERVICE_MESSAGE, { chatId, serviceType, messageId });
            resolve(true)
        }
        );
    },
    [HANDLE_READ_MESSAGES]: ({ commit }, { chatId, messagesIds }) => {
        return new Promise((resolve) => {
            commit(HANDLE_READ_MESSAGES, { chatId, messagesIds });
            resolve(true)
        }
        );
    },
    [ADD_CHAT]: ({ commit, getters }, chat) => {
        return new Promise((resolve) => {
            commit(ADD_CHAT, { chat: chat, selfId: getters.selfId });
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
    [ADD_MESSAGE]: ({ commit }, { chatId, message }) => {
        return new Promise((resolve) => {
            commit(ADD_MESSAGE, { chatId, message });
            resolve(true)
        }
        );
    },
    [HANDLE_USER_STATUS_MESSAGE]: ({ commit }, { chatId, status }) => {
        return new Promise((resolve) => {
            commit(HANDLE_USER_STATUS_MESSAGE, { chatId, status });
            resolve(true)
        }
        );
    },
    // [SET_SELF_ID]: ({ commit, rootGetters }) => {
    //     return new Promise((resolve) => {
    //         commit(SET_SELF_ID, rootGetters.id);
    //         resolve(true)
    //     }
    //     );
    // },
    [SET_READ_MSGS_NOTIFIER]: ({ commit }, readMsgsNotifier) => {
        return new Promise((resolve) => {
            commit(SET_READ_MSGS_NOTIFIER, readMsgsNotifier);
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
    [SET_CHATS_VISIBLE]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(SET_CHATS_VISIBLE);
            resolve(true)
        }
        );
    },
    [SET_CHATS_UNVISIBLE]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(SET_CHATS_UNVISIBLE);
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
    [SET_CHAT_WINDOW_OPEN]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(SET_CHAT_WINDOW_OPEN);
            resolve(true)
        }
        );
    },
    [SET_CHAT_WINDOW_CLOSE]: ({ commit }) => {
        return new Promise((resolve) => {
            commit(SET_CHAT_WINDOW_CLOSE);
            resolve(true)
        }
        );
    },
    [SET_CHAT_SOCKET]: ({ commit }, chatSocket) => {
        return new Promise((resolve) => {
            commit(SET_CHAT_SOCKET, chatSocket);
            resolve(true)
        }
        );
    },
};
const mutations = {
    [SET_ACTIVE_CHAT]: (state, { chatId, chat, selfId }) => {
        state.activeChatId = chatId;
        state.activeChatMessages = state.messages.get(chatId);
        state.activeChatMessagesNextPage = state.messagesPages.get(chatId) == undefined ? 1 : state.messagesPages.get(chatId)
        // const chat = state.chats.find(chat => chat.id === chatId)
        state.activeChatMembers = chat.members;
        state.activeChatOpponentId = chat.members.find(member => member.id != selfId).id;
        // state.activeChatOpponentId = chat.members.find(member => member.id != state.selfId).id;
        state.activeChatTitle = chat.title;
        let counter = false
        // if (!chat.opened) {
        var chats = state.chats
        chats.forEach(item => {
            if (item.id == chatId) {
                item.opened = true
                item.messages__count = 0
            }
            if (item.messages__count > 0) {
                counter = true
                // для отображения иконки новых сообщений в списке чатов
            }
        })
        state.chats = chats
        if (counter) {
            // для отображения иконки новых сообщений в списке чатов
            state.newMessages = true
        } else {
            state.newMessages = false
        }
        // }
        let msgs = state.messages.get(chatId)
        let unread_messages = msgs.filter(msg => {
            return !msg.read_by_the_user && msg.sender == state.activeChatOpponentId
        })
        if (unread_messages.length > 0) {
            state.messages = check_read_msgs(state, chatId, msgs)
        }
    },
    [SET_CHATS]: (state, { chats, selfId }) => {
        console.log(chats, selfId)
        chats.forEach(item => {
            // item.title = item.members.find(member => member.id != state.selfId).fio
            item.title = item.members.find(member => member.id != selfId).fio
            item.opened = false
            return item
        });
        state.chats = chats;
    },
    [ADD_CHAT]: (state, { chat, selfId }) => {
        // chat.title = chat.members.find(member => member.id != state.selfId).fio
        chat.title = chat.members.find(member => member.id != selfId).fio
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
        // state.messages.set(chatId, msgs)
        let unread_messages = msgs.filter(msg => {
            return !msg.read_by_the_user && msg.sender == state.activeChatOpponentId
        })
        if (unread_messages.length > 0) {
            msgs = check_read_msgs(state, chatId, msgs)
        }
        state.messages.set(chatId, msgs)

    },
    [ADD_MESSAGE]: (state, { chatId, message }) => {
        // продумать добавление при незагруженных чатах
        let chat = state.chats.find(chat => chat.id == chatId)
        if (chat != undefined) {
            if (state.chatsVisible) {
                state.newMessages = true
            }
            // console.log("chat handle")
            if (chat.opened) {
                // console.log("opened", 'chatId', chatId)
                let msgs = state.messages.get(chatId)
                // console.log(msgs)
                msgs.push(message);
                state.messages.set(chatId, msgs)
            }
            if (!chat.dialog_is_not_empty) {
                let chats = state.chats
                chats.forEach(item => {
                    if (item.id == chat.id) {
                        item.dialog_is_not_empty = true
                    }
                })
                state.chats = chats
            }
            // console.log("chat no opened")
            if (state.chatsVisible) {
                state.newMessages = true
                if (typeof (chat.messages__count) == 'number') {
                    chat.messages__count += 1
                } else {
                    chat.messages__count = 1
                }
                let chats = state.chats
                chats.forEach(item => {
                    if (item.id == chat.id) {
                        item = chat
                    }
                })
                state.chats = chats
            }
        }
    },
    [HANDLE_USER_STATUS_MESSAGE]: (state, { chatId, status }) => {
        let chats = state.chats
        chats.forEach(item => {
            if (item.id == chatId) {
                item.online = status
            }
        })
        state.chats = chats
    },
    [HANDLE_SERVICE_MESSAGE]: (state, { chatId, serviceType, messageId }) => {
        let msgs = state.messages.get(chatId)
        msgs.forEach(item => {
            if (item.id == messageId) {
                if (serviceType == 'sent') {
                    item.sent_by_the_server = true
                } else if (serviceType == "message_received") {
                    item.received_by_the_user = true
                    // } else if (serviceType == "messages_read") {
                    //     item.read_by_the_user = true
                } else if (serviceType == "message_received_and_read") {
                    item.read_by_the_user = true
                    item.received_by_the_user = true
                }
            }
        })
        state.messages.set(chatId, msgs)
    },
    [HANDLE_READ_MESSAGES]: (state, { chatId, messagesIds }) => {
        let msgs = state.messages.get(chatId)
        if (msgs != undefined) {
            msgs.forEach(item => {
                if (messagesIds.indexOf(item.id) != -1) {
                    item.read_by_the_user = true
                }
            })
            state.messages.set(chatId, msgs)
        }
    },
    [SET_MESSAGES_PAGE]: (state, { chatId, nextPage }) => {
        state.messagesPages.set(chatId, nextPage)
    },
    // [SET_SELF_ID]: (state, selfId) => {
    //     state.selfId = selfId
    // },
    [SET_READ_MSGS_NOTIFIER]: (state, readMsgsNotifier) => {
        state.readMsgsNotifier = readMsgsNotifier
    },
    [TOOGLE_CHATS_VISIBLE]: (state) => {
        state.chatsVisible = !state.chatsVisible
    },
    [SET_CHATS_VISIBLE]: (state) => {
        state.chatsVisible = true
    },
    [SET_CHATS_UNVISIBLE]: (state) => {
        state.chatsVisible = false
    },
    [SET_NEW_MESSAGES]: (state) => {
        state.newMessages = true
    },
    [UNSET_NEW_MESSAGES]: (state) => {
        state.newMessages = false
    },
    [SET_CHAT_WINDOW_OPEN]: (state) => {
        state.chatWindowIsOpen = true
    },
    [SET_CHAT_WINDOW_CLOSE]: (state) => {
        state.chatWindowIsOpen = false
    },
    [SET_CHAT_SOCKET]: (state, chatSocket) => {
        state.chatSocket = chatSocket
    },

};

export default {
    state,
    getters,
    actions,
    mutations
};