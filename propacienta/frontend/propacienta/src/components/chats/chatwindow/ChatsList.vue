<template>
  <div class="chat-list" :style="{ background: userListColor.userList.bg }">
    <!-- <v-row v-for="user in chats" :key="user.id" @click="$emit('chat', user.id)">
      <v-col><img :src="user.imageUrl" class="img-msg" /></v-col>
      <v-col>{{ user.name }}</v-col> -->

    <table style="padding-top: 5px">
      <tbody>
        <tr
          v-for="chat in chats"
          :key="chat.id"
          @click="$emit('chat', chat.id)"
        >
          <td style="text-align: center">
            <v-badge dot :color="chat.online ? 'green' : 'red'" overlap>
              <img :src="imageUrl(chat)" class="img-msg" />
            </v-badge>
          </td>
          <td
            class="chat-element"
            :style="{
              color: userListColor.userList.text,
            }"
          >
            {{ chatName(chat) }}
          </td>
          <td v-if="newMessages(chat)">
            <v-icon color="light-blue lighten-2"> mdi-message</v-icon>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- </v-row> -->
  </div>
</template>

<script>
export default {
  props: {
    chats: {
      type: Array,
      required: true,
    },
    colors: {
      type: Object,
      default: () => ({}),
    },
  },
  methods: {
    chatName: function (chat) {
      const selfId = this.$store.getters.id;
      const members = chat.members.filter((item) => {
        return item.id != selfId;
      });
      return members[0].fio;
    },
    newMessages: function (chat) {
      return chat.messages__count > 0;
    },
    imageUrl: function (chat) {
      const selfId = this.$store.getters.id;
      const members = chat.members.filter((item) => {
        return item.id != selfId;
      });
      if (members[0].doctor_id != null) {
        return members[0].doctor_foto != null
          ? members[0].doctor_foto
          : require("@/assets/default_doctor_avatar.png");
      } else {
        return require("@/assets/default-pacient.jpg");
      }
    },
  },
  computed: {
    userListColor() {
      const defaultColors = {
        userList: {
          bg: "#FFFFFF",
          text: "#000000",
        },
      };
      return Object.assign(defaultColors, this.colors);
    },
  },
};
</script>

<style scoped>
.chat-list {
  height: 100%;
  overflow: auto;
  padding-left: 5px;
  padding-top: 8px;
  border-bottom-left-radius: 9px;
  border-bottom-right-radius: 9px;
}
.img-msg {
  border-radius: 50%;
  width: 40px;
  object-fit: cover;
  height: 40px;
  margin-right: 5px;
}
.chat-element {
  font-size: 17px;
  vertical-align: middle;
}
</style>
