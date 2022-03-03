<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="cyan darken-1">
            <v-toolbar-title>Активация регистрации</v-toolbar-title>
          </v-toolbar>
          <v-card-text v-if="activationOnLoad" class="text-center">
            <v-progress-circular
              :size="70"
              :width="7"
              color="cyan darken-2"
              indeterminate
            ></v-progress-circular>
          </v-card-text>
          <v-card-text v-if="activateRegistrationStatus">
            Активация выполнена. Пожалуйста, авторизуйтесь.
          </v-card-text>
          <v-card-text v-if="activateRegistrationError">
            Ошибка активации. Перезагрузите страницу или обратитесь к
            администрации сервиса.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="cyan"
              v-on:click="onOk"
              :disabled="!activateRegistrationStatus"
              >Ok</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import {
  ACTIVATE_REGISTRATION_REQUEST,
  ACTIVATE_ON_LOAD,
} from "@/store/actions/registration";
export default {
  name: "ActivateRegistrationView",
  props: {
    source: String,
  },
  // data: function () {
  //   return {};
  // },
  computed: {
    activationOnLoad: function () {
      return this.$store.getters.activateOnLoad;
    },
    activateRegistrationStatus: function () {
      return this.$store.getters.activateRegistrationStatus;
    },
    activateRegistrationError: function () {
      return this.$store.getters.activateRegistrationError;
    },
  },
  methods: {
    onOk: function () {
      this.$router.push({ name: "login" });
    },
  },
  mounted: async function () {
    let data = {
      uid: this.$route.params.uid,
      token: this.$route.params.token,
    };
    await this.$store.dispatch(ACTIVATE_ON_LOAD);
    await this.$store.dispatch(ACTIVATE_REGISTRATION_REQUEST, data);
  },
};
</script>

<style>
.v-btn__content {
  color: white;
}
/* .shake {
  width: 200px;
  height: 50px;
} */
.shake {
  -webkit-animation: 1.2s ease-in-out 0s normal none 1 running
    trambling-animation;
  -moz-animation: 1.2s ease-in-out 0s normal none 1 running trambling-animation;
  -o-animation: 1.2s ease-in-out 0s normal none 1 running trambling-animation;
  animation: 1.2s ease-in-out 0s normal none 1 running trambling-animation;
}
@keyframes trambling-animation {
  0%,
  50%,
  100% {
    transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    -ms-transform: rotate(0deg);
  }
  10%,
  30% {
    transform: rotate(-3deg);
    -webkit-transform: rotate(-3deg);
    -moz-transform: rotate(-3deg);
    -o-transform: rotate(-3deg);
    -ms-transform: rotate(-3deg);
  }
  20%,
  40% {
    transform: rotate(3deg);
    -webkit-transform: rotate(3deg);
    -moz-transform: rotate(3deg);
    -o-transform: rotate(3deg);
    -ms-transform: rotate(3deg);
  }
}
</style>
