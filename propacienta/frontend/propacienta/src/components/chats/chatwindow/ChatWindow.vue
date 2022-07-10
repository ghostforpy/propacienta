<template>
  <div class="sc-chat-window" :class="{ opened: isOpen, closed: !isOpen }">
    <Header
      v-if="showHeader"
      :title="computedTitle"
      :showChats="showChatsList"
      :colors="colors"
      @close="$emit('close')"
      @chatsList="handleChatsListToggle"
    >
      <template>
        <slot name="header"> </slot>
      </template>
    </Header>
    <ChatsList
      v-if="showChatsList"
      :colors="colors"
      :chats="chats"
      @chat="handleChat"
    />
    <MessageList
      v-if="!showChatsList"
      :messages="messages"
      :participants="members"
      :show-typing-indicator="showTypingIndicator"
      :colors="colors"
      :always-scroll-to-bottom="alwaysScrollToBottom"
      :message-styling="messageStyling"
      @scrollToTop="$emit('scrollToTop')"
      @remove="$emit('remove', $event)"
    >
      <template v-slot:user-avatar="scopedProps">
        <slot
          name="user-avatar"
          :user="scopedProps.user"
          :message="scopedProps.message"
        >
        </slot>
      </template>
      <template v-slot:text-message-body="scopedProps">
        <slot
          name="text-message-body"
          :message="scopedProps.message"
          :messageText="scopedProps.messageText"
          :messageColors="scopedProps.messageColors"
          :me="scopedProps.me"
        >
        </slot>
      </template>
      <template v-slot:system-message-body="scopedProps">
        <slot name="system-message-body" :message="scopedProps.message"> </slot>
      </template>
      <template v-slot:text-message-toolbox="scopedProps">
        <slot
          name="text-message-toolbox"
          :message="scopedProps.message"
          :me="scopedProps.me"
        >
        </slot>
      </template>
    </MessageList>
    <!-- :suggestions="getSuggestions()" -->
    <UserInput
      v-if="!showChatsList"
      :show-emoji="showEmoji"
      :on-submit="onUserInputSubmit"
      :show-file="showFile"
      :placeholder="placeholder"
      :colors="colors"
      @onType="$emit('onType')"
      @edit="$emit('edit', $event)"
    />
  </div>
</template>

<script>
import Header from "./HeaderChatWindow.vue";
import MessageList from "./MessageList.vue";
import UserInput from "./UserInput.vue";
import ChatsList from "./ChatsList.vue";
import { SET_ACTIVE_CHAT, TOOGLE_CHATS_VISIBLE } from "@/store/actions/chats";
export default {
  components: {
    Header,
    MessageList,
    UserInput,
    ChatsList,
  },
  props: {
    showEmoji: {
      type: Boolean,
      default: false,
    },
    showFile: {
      type: Boolean,
      default: false,
    },
    showHeader: {
      type: Boolean,
      default: true,
    },
    chats: {
      type: Array,
      required: true,
    },
    participants: {
      type: Array,
      required: false,
    },
    title: {
      type: String,
      required: true,
    },
    onUserInputSubmit: {
      type: Function,
      required: true,
    },
    messageList: {
      type: Array,
      default: () => [],
    },
    isOpen: {
      type: Boolean,
      default: () => false,
    },
    placeholder: {
      type: String,
      required: true,
    },
    showTypingIndicator: {
      type: String,
      required: true,
    },
    colors: {
      type: Object,
      required: true,
    },
    alwaysScrollToBottom: {
      type: Boolean,
      required: true,
    },
    messageStyling: {
      type: Boolean,
      required: true,
    },
    // readMsgsNotifier: {
    //   type: Function,
    //   required: true,
    // },
  },
  // data() {
  //   return {
  //     // showChatsList: true,
  //   };
  // },
  computed: {
    members() {
      return this.$store.getters.activeChatMembers;
    },
    messages() {
      // let messages = this.messageList;
      return this.$store.getters.activeChatMessages;
    },
    computedTitle() {
      return !this.showChatsList ? this.title : "Мои сообщения";
    },
    showChatsList() {
      return this.$store.getters.chatsVisible;
    },
  },
  methods: {
    handleChatsListToggle() {
      // this.showChatsList = showChatsList;
      this.$store.dispatch(TOOGLE_CHATS_VISIBLE);
    },
    async handleChat(chatId) {
      // console.log(chatId);
      // await this.$store.dispatch(GET_MESSAGES, chatId);
      // var el = this;
      this.$store.dispatch(SET_ACTIVE_CHAT, {
        chatId: chatId,
        // readMsgsNotifier: this.readMsgsNotifier,
      });
      // .then(() => {
      // el.showChatsList = false;
      // }
      // );
      this.$store.dispatch(TOOGLE_CHATS_VISIBLE);
      // this.$emit("activeChat", chatId);
    },
    getSuggestions() {
      return this.messages.length > 0
        ? this.messages[this.messages.length - 1].suggestions
        : [];
    },
  },
};
</script>

<style scoped>
.sc-chat-window {
  width: 370px;
  height: calc(100% - 120px);
  max-height: 590px;
  position: fixed;
  right: 25px;
  bottom: 100px;
  box-sizing: border-box;
  box-shadow: 0px 7px 40px 2px rgba(148, 149, 150, 0.1);
  background: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 10px;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  animation: fadeIn;
  animation-duration: 0.3s;
  animation-timing-function: ease-in-out;
}

.sc-chat-window.closed {
  opacity: 0;
  display: none;
  bottom: 90px;
}

@keyframes fadeIn {
  0% {
    display: none;
    opacity: 0;
  }

  100% {
    display: flex;
    opacity: 1;
  }
}

.sc-message--me {
  text-align: right;
}
.sc-message--them {
  text-align: left;
}

@media (max-width: 450px) {
  .sc-chat-window {
    width: 100%;
    height: 100%;
    max-height: 100%;
    right: 0px;
    bottom: 0px;
    border-radius: 0px;
  }
  .sc-chat-window {
    transition: 0.1s ease-in-out;
  }
  .sc-chat-window.closed {
    bottom: 0px;
  }
}
</style>
