<template>
  <div class="sc-message--text" :style="messageColors">
    <template>
      <div
        class="sc-message--toolbox"
        :style="{ background: messageColors.backgroundColor }"
      >
        <button
          v-if="showEdition && me && message.id"
          :disabled="isEditing"
          @click="edit"
        >
          <IconBase
            :color="isEditing ? 'black' : messageColors.color"
            width="10"
            icon-name="edit"
          >
            <IconEdit />
          </IconBase>
        </button>
        <button
          v-if="showDeletion && me && message.id"
          @click="$emit('remove')"
        >
          <IconBase :color="messageColors.color" width="10" icon-name="remove">
            <IconCross />
          </IconBase>
        </button>
        <slot name="text-message-toolbox" :message="message" :me="me"> </slot>
      </div>
    </template>
    <slot
      :message="message"
      :messageText="messageText"
      :messageColors="messageColors"
      :me="me"
    >
      <div class="sc-message--text-content" v-html="messageText"></div>
      <span
        v-if="message.created_at"
        class="sc-message--meta sc-message-created-at"
        :style="{ color: messageColors.color }"
      >
        {{ time }}
      </span>
      <!-- <p
        v-if="message.meta"
        class="sc-message--meta"
        :style="{ color: messageColors.color }"
      >
        {{ message.meta }}
      </p> -->
      <!-- <p v-if="message.isEdited" class="sc-message--edited">
        <IconBase width="10" icon-name="edited">
          <IconEdit />
        </IconBase>
        edited
      </p> -->
    </slot>
  </div>
</template>

<script>
import { mapState } from "../store/";
import IconBase from "./../components/IconBase.vue";
import IconEdit from "./../components/icons/IconEdit.vue";
import IconCross from "./../components/icons/IconCross.vue";
import escapeGoat from "escape-goat";
import Autolinker from "autolinker";
import store from "../store/";

const fmt = require("msgdown");

export default {
  components: {
    IconBase,
    IconCross,
    IconEdit,
  },
  props: {
    message: {
      type: Object,
      required: true,
    },
    messageColors: {
      type: Object,
      required: true,
    },
    messageStyling: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    time() {
      let ms = new Date(this.message.created_at);
      return `${ms.toLocaleDateString()}, ${ms
        .toLocaleTimeString()
        .slice(0, 5)}`;
    },
    messageText() {
      // console.log(this.message);
      const escaped = escapeGoat.escape(this.message.message);

      return Autolinker.link(this.messageStyling ? fmt(escaped) : escaped, {
        className: "chatLink",
        truncate: { length: 50, location: "smart" },
      });
    },
    me() {
      return this.message.sender === this.$store.getters.id;
    },
    isEditing() {
      return (
        (store.state.editMessage && store.state.editMessage.id) ===
        this.message.id
      );
    },
    ...mapState(["showDeletion", "showEdition"]),
  },
  methods: {
    edit() {
      store.setState("editMessage", this.message);
    },
  },
};
</script>

<style scoped lang="scss">
.sc-message-created-at {
  align-self: end;
}
.sc-message--text {
  display: flex;
  flex-direction: column;
  padding: 5px 10px;
  border-radius: 6px;
  font-weight: 300;
  font-size: 14px;
  line-height: 1.4;
  position: relative;
  -webkit-font-smoothing: subpixel-antialiased;
  .sc-message--text-content {
    align-self: start;
    white-space: pre-wrap;
  }
  &:hover .sc-message--toolbox {
    left: -20px;
    opacity: 1;
  }
  .sc-message--toolbox {
    transition: left 0.2s ease-out 0s;
    white-space: normal;
    opacity: 0;
    position: absolute;
    left: 0px;
    width: 25px;
    top: 0;
    button {
      background: none;
      border: none;
      padding: 0px;
      margin: 0px;
      outline: none;
      width: 100%;
      text-align: center;
      cursor: pointer;
      &:focus {
        outline: none;
      }
    }
    // & /deep/ svg {
    //   margin-left: 5px;
    // }
  }
  code {
    font-family: "Courier New", Courier, monospace !important;
  }
}

.sc-message--content.sent .sc-message--text {
  color: white;
  background-color: #4e8cff;
  max-width: calc(100% - 120px);
  word-wrap: break-word;
}

.sc-message--content.received .sc-message--text {
  color: #263238;
  background-color: #f4f7f9;
  margin-right: 40px;
}

a.chatLink {
  color: inherit !important;
}
</style>
