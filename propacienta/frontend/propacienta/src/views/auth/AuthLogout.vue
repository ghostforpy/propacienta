<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="cyan darken-1">
            <v-toolbar-title>Выход</v-toolbar-title>
          </v-toolbar>
          <v-card-text> Вы точно хотите выйти из системы? </v-card-text>
          <div v-if="logoutError" v-bind:class="{ shake: animError }">
            <v-alert transition="fade-transition" type="error">
              {{ logoutErrorText }}
            </v-alert>
          </div>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="red accent-2"
              class="white-content"
              v-on:click="onSubmitExit"
              >Выход</v-btn
            >
            <v-btn
              color="cyan"
              class="white-content"
              v-on:click="$router.go(-1)"
              >Отмена</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { AUTH_LOGOUT } from "@/store/actions/auth";
export default {
  name: "AuthLogout",
  props: {
    source: String,
  },
  data: function () {
    return {
      logoutError: false,
      animError: false,
    };
  },
  computed: {
    logoutErrorText: function () {
      if (this.logoutError) {
        if (this.$store.getters.logoutErrorStatus == 403) {
          return "Ошибка учетных данных";
        }
      }
      return "Сервер недоступен";
    },
  },
  methods: {
    onSubmitExit: async function () {
      this.animError = false;
      const res = await this.$store.dispatch(AUTH_LOGOUT);
      if (res) {
        this.$router.push({
          path: "/",
        });
        this.logoutError = false;
      } else {
        if (this.logoutError) {
          this.animError = true;
        }
        this.logoutError = true;
      }
    },
  },
};
</script>

<style>
.white-content.v-btn {
  color: white;
}
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
