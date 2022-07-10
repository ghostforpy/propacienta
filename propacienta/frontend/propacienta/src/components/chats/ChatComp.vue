<template>
  <div style="z-index: 10">
    <Chat
      :onMessageWasSent="onMessageWasSent"
      :newMessagesCount="newMessagesCount"
      :isOpen="isChatOpen"
      :close="closeChat"
      :open="openChat"
      :showEmoji="false"
      placeholder="Сообщение..."
      :showFile="false"
      :showEdition="false"
      :showDeletion="false"
      :showTypingIndicator="showTypingIndicator"
      :showLauncher="true"
      :showCloseButton="true"
      :colors="colors"
      :alwaysScrollToBottom="alwaysScrollToBottom"
      :disableUserListToggle="false"
      :messageStyling="messageStyling"
      @onType="handleOnType"
      @edit="editMessage"
    />
  </div>
</template>
<script>
import Chat from "./chatwindow/LauncherChat";
import { BASE_URL } from "@/api/HTTP";
import ReconnectingWebSocket from "reconnecting-websocket";
import {
  ADD_MESSAGE,
  HANDLE_SERVICE_MESSAGE,
  HANDLE_USER_STATUS_MESSAGE,
  HANDLE_READ_MESSAGES,
  SET_READ_MSGS_NOTIFIER,
  SET_NEW_MESSAGES,
  SET_CHATS_VISIBLE,
} from "@/store/actions/chats";
export default {
  name: "ChatComp",
  components: {
    Chat,
  },
  data() {
    return {
      // messageList: [
      //   { type: "text", author: `me`, data: { text: `Say yes!` } },
      //   { type: "text", author: `user1`, data: { text: `No.` } },
      // ], // the list of the messages to show, can be paginated and adjusted dynamically
      chatSocket: null,
      newMessagesCount: this.$store.getters.newMessages,
      isChatOpen: false, // to determine whether the chat window should be open or closed
      showTypingIndicator: "", // when set to a value matching the participant.id it shows the typing indicator for the specific user
      colors: {
        header: {
          bg: "#4e8cff",
          text: "#ffffff",
        },
        launcher: {
          bg: "#4e8cff",
        },
        messageList: {
          bg: "#ffffff",
        },
        sentMessage: {
          bg: "#4e8cff",
          text: "#ffffff",
        },
        receivedMessage: {
          bg: "#eaeaea",
          text: "#222222",
        },
        userInput: {
          bg: "#f4f7f9",
          text: "#565867",
        },
      }, // specifies the color scheme for the component
      alwaysScrollToBottom: false, // when set to true always scrolls the chat to the bottom when new events are in (new message, user starts typing...)
      messageStyling: true, // enables *bold* /emph/ _underline_ and such (more info at github.com/mattezza/msgdown)
    };
  },
  mounted() {
    // console.log("mounteed");
    // const TIMEOUT = 1000;
    // const chatSocket = new WebSocket("ws://" + BASE_URL + "/ws/chats/");
    this.chatSocket = new ReconnectingWebSocket(
      "ws://" + BASE_URL + "/ws/chats/"
    );
    this.chatSocket.timeoutInterval = 5400;
    // this.chatSocket.onopen = function (e) {
    //   console.log("WS open", e);
    // };
    var el = this;
    this.chatSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      el.onMessageMainHandler(data);
    };
    this.$store.dispatch(SET_READ_MSGS_NOTIFIER, this.readMsgsNotifier);
    // this.chatSocket.onclose = function (e) {
    //   console.error(e, "Chat socket closed unexpectedly");
    // };
  },
  methods: {
    readMsgsNotifier(messages_ids, dialog_id, sender_id) {
      // console.log(
      //   "handle readMsgsNotifier",
      //   messages_ids,
      //   dialog_id,
      //   sender_id
      // );
      this.sendServiceMessage({
        service_type: "messages_read",
        messages_ids: messages_ids,
        dialog: dialog_id,
        sender: sender_id,
      });
    },
    sendServiceMessage(message) {
      this.chatSocket.send(
        JSON.stringify({
          type: "service",
          message: message,
        })
      );
    },
    onMessageMainHandler(data) {
      if (data.type == "message") {
        this.messageHandler(data);
      } else if (data.type == "service") {
        this.serviceHandler(data);
      }
    },
    messageHandler(data) {
      // console.log(data);
      if (!this.isChatOpen) {
        this.$store.dispatch(SET_NEW_MESSAGES);
      }
      this.$store.dispatch(ADD_MESSAGE, {
        chatId: data.message.dialog,
        message: data.message,
      });
      if (data.message.sender != this.$store.getters.id) {
        if (
          data.message.dialog == this.$store.getters.activeChatId &&
          this.isChatOpen &&
          !this.$store.getters.chatsVisible
        ) {
          this.sendServiceMessage({
            service_type: "message_received_and_read",
            message_id: data.message.id,
            dialog: data.message.dialog,
            sender: data.message.sender,
          });
        } else {
          this.sendServiceMessage({
            service_type: "message_received",
            message_id: data.message.id,
            dialog: data.message.dialog,
            sender: data.message.sender,
          });
        }
      }
    },
    serviceHandler(data) {
      if (data.service_type == "typing") {
        console.log("handle typing", data);
      } else if (data.service_type == "newchat") {
        console.log("handle new chat", data);
      } else if (data.service_type == "user_status") {
        // console.log("handle user status msg", data);
        this.$store.dispatch(HANDLE_USER_STATUS_MESSAGE, {
          chatId: data.dialog,
          status: data.user_status,
        });
      } else if (data.service_type == "messages_read") {
        this.$store.dispatch(HANDLE_READ_MESSAGES, {
          chatId: data.dialog,
          // serviceType: data.service_type,
          messagesIds: data.messages_ids,
        });
      } else {
        // service_type in [sent, delivered, read]
        // console.log(data);
        this.$store.dispatch(HANDLE_SERVICE_MESSAGE, {
          chatId: data.dialog,
          serviceType: data.service_type,
          messageId: data.message_id,
        });
      }
    },
    sendMessage(text) {
      if (text.length > 0) {
        this.newMessagesCount = this.isChatOpen
          ? this.newMessagesCount
          : this.newMessagesCount + 1;
        this.onMessageWasSent(
          JSON.stringify({
            sender: this.$store.getters.id, // user id
            chat: this.$store.getter.activeChatId,
            send: new Date(),
            type: "text",
            data: { text },
          })
        );
      }
    },
    onMessageWasSent(message) {
      // called when the user sends a message
      // console.log(message);
      this.chatSocket.send(message);
      // this.messageList = [...this.messageList, message];
    },
    openChat() {
      // called when the user clicks on the fab button to open the chat
      this.isChatOpen = true;
      this.newMessagesCount = 0;
    },
    closeChat() {
      // called when the user clicks on the botton to close the chat
      this.isChatOpen = false;
      this.$store.dispatch(SET_CHATS_VISIBLE);
    },
    // handleScrollToTop() {
    // called when the user scrolls message list to top
    // leverage pagination for loading another page of messages
    // },
    handleOnType() {
      // console.log("Emit typing event");
    },
    editMessage(message) {
      const m = this.messageList.find((m) => m.id === message.id);
      m.isEdited = true;
      m.data.text = message.data.text;
    },
  },
};
</script>