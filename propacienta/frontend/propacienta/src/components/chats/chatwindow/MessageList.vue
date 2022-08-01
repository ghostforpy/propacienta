<template>
  <div
    ref="scrollList"
    class="sc-message-list"
    :style="{ backgroundColor: colors.messageList.bg }"
    @scroll="handleScroll"
  >
    <Message
      v-for="(message, idx) in messages"
      :key="idx"
      :message="message"
      :user="profile(message.sender)"
      :colors="colors"
      :message-styling="messageStyling"
      @remove="$emit('remove', message)"
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
    </Message>
    <Message
      v-show="showTypingIndicator !== ''"
      :message="{ author: showTypingIndicator, type: 'typing' }"
      :user="profile(showTypingIndicator)"
      :colors="colors"
      :message-styling="messageStyling"
    />
  </div>
</template>

<script>
import Message from "./MessageItem.vue";
import chatIcon from "./assets/chat-icon.svg";

export default {
  components: {
    Message,
  },
  data() {
    return {
      firstload: true,
    };
  },
  props: {
    participants: {
      type: Array,
      required: true,
    },
    messages: {
      type: Array,
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
  },
  computed: {
    defaultChatIcon() {
      return chatIcon;
    },
  },
  // mounted() {
  //   this.$nextTick(this._scrollDown());
  // },
  updated() {
    // console.log("upd");
    // if (this.firstload) {
    //   console.log("first");
    //   this.firstload = false;
    //   this.$nextTick(this._scrollDown());
    // }
    if (this.alwaysScrollToBottom) this.$nextTick(this._scrollDown());
  },
  mounted() {
    // console.log("mnt");
    if (this.shouldScrollToBottom()) this.$nextTick(this._scrollDown());
  },
  methods: {
    _scrollDown() {
      this.$refs.scrollList.scrollTop = this.$refs.scrollList.scrollHeight;
      // при монтировании не скролится
      // console.log(
      //   "_scrollDown",
      //   this.$refs.scrollList.scrollHeight,
      //   this.$refs.scrollList.scrollTop
      // );
    },
    handleScroll(e) {
      if (e.target.scrollTop === 0) {
        this.$emit("scrollToTop");
      }
    },
    shouldScrollToBottom() {
      const scrollTop = this.$refs.scrollList.scrollTop;
      // const scrollable = scrollTop > this.$refs.scrollList.scrollHeight - 500;
      const scrollable =
        this.$refs.scrollList.scrollHeight - scrollTop - 300 > 0;

      // console.log(
      //   "shouldScrollToBottom",
      //   this.$refs.scrollList.scrollTop,
      //   this.$refs.scrollList.scrollHeight,
      //   this.alwaysScrollToBottom || scrollable
      // );

      return this.alwaysScrollToBottom || scrollable;
    },
    profile(author) {
      const profile = this.participants.find(
        (profile) => profile.id === author
      );
      // A profile may not be found for system messages or messages by 'me'
      return profile || { imageUrl: "", name: "" };
    },
  },
};
</script>

<style scoped>
.sc-message-list {
  height: 80%;
  overflow-y: auto;
  background-size: 100%;
  padding: 40px 20px;
}
</style>
