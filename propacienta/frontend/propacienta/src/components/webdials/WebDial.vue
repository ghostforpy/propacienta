<template>
  <div>
    <v-btn
      small
      class="mt-2 white-content"
      style="width: 100%"
      color="cyan lighten-2"
      rounded
      @click="callHandler"
    >
      Позвонить
    </v-btn>
    <v-card
      :loading="dialInProgress"
      height="220"
      width="150"
      color="grey"
      class="dial-card-posiotion"
      v-if="dialCardShow"
    >
      <v-img
        v-if="!dialWithRemoteVideo"
        class="grey-background"
        height="150"
        contain
        :src="avatarSrc"
      ></v-img>
      <v-card-text class="text-center">
        <v-btn fab small color="red lighten-1" @click="discardCallHandler"
          ><v-icon color="white" class="rotate-dial">mdi-phone</v-icon></v-btn
        >
      </v-card-text>
    </v-card>
  </div>
</template>
<script>
export default {
  name: "WebDial",
  // props: {
  //   id: Number,
  //   firstName: String,
  //   lastName: String,
  //   patronymic: String,
  //   birthday: String,
  // },
  data: function () {
    return {
      dialCardShow: false,
      dialInProgress: true,
      dialWithRemoteVideo: false,
      localVideo: false,
    };
  },
  computed: {
    avatarSrc: function () {
      return require("@/assets/doctor_dial_avatar.jpeg");
    },
  },
  methods: {
    callHandler() {
      console.log("call handler");
      this.dialCardShow = true;
    },
    discardCallHandler() {
      console.log("discardCallHandler");
      this.dialCardShow = false;
    },
  },
};
</script>
<style>
.break-word {
  word-break: break-word;
}
.dial-card-posiotion {
  position: absolute;
  right: 10px;
  top: 10px;
}
.rotate-dial {
  transform: rotate(135deg);
}
.grey-background {
  background: grey;
}
</style>