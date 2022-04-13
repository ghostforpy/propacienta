<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="cyan darken-1">
            <v-toolbar-title>Сброс пароля</v-toolbar-title>
          </v-toolbar>
          <v-card-text v-if="!okSender">
            <v-form>
              <v-text-field
                id="password"
                name="password"
                label="Пароль"
                type="password"
                v-model="password"
                ref="password"
                :rules="[
                  (value) => !!value || 'Это поле является обязательным.',
                ]"
              ></v-text-field>
              <v-text-field
                id="re_password"
                name="re_password"
                label="Повторите пароль"
                type="password"
                v-model="re_password"
                ref="re_password"
                :rules="[
                  (value) => !!value || 'Это поле является обязательным.',
                ]"
              ></v-text-field>
            </v-form>
            <div v-if="sendError" v-bind:class="{ shake: animError }">
              <v-alert transition="fade-transition" type="error">
                {{ sendErrorText }}
              </v-alert>
            </div>
          </v-card-text>
          <v-card-text v-else> Пароль успешно изменен. </v-card-text>
          <v-card-actions>
            <v-btn
              class="white-content"
              color="cyan"
              v-on:click="onSubmit"
              v-if="!okSender"
              block
              :disabled="!submitAvailable"
              >Отправить</v-btn
            >
            <v-btn
              class="white-content"
              color="cyan"
              :to="{ name: 'login' }"
              v-else
              block
            >
              Ok</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import request_service from "@/api/HTTP";
export default {
  name: "PasswordForgotConfirm",
  props: {
    source: String,
  },
  data: function () {
    return {
      email: null,
      password: null,
      re_password: null,
      okSender: false,
      animError: false,
      sendError: false,
      sendErrorText: "Что-то пошло не так. Попробуйте позже.",
    };
  },
  computed: {
    submitAvailable: function () {
      const v =
        this.password != null &&
        this.password != "" &&
        this.re_password != null &&
        this.re_password != "" &&
        this.password === this.re_password;
      return v;
    },
  },
  methods: {
    onSubmit: async function () {
      if (this.password != this.re_password) {
        if (this.registrationError) {
          this.animError = true;
        }
        this.registrationError = true;
        return;
      }
      let data = {
        uid: this.$route.params.uid,
        token: this.$route.params.token,
        new_password: this.password,
      };
      let config = {
        method: "post",
        url: `api/users/reset_password_confirm/`,
        data: data,
      };
      var el = this;
      this.animError = false;
      request_service(
        config,
        function () {
          el.okSender = true;
          el.sendError = false;
        },
        function (error) {
          if (error.response.status == 400) {
            if (error.response.data.new_password != undefined) {
              el.sendErrorText = "";
              error.response.data.new_password.map((item) => {
                el.sendErrorText += " " + item;
              });
            }
          } else {
            el.sendErrorText = "Что-то пошло не так. Попробуйте позже.";
          }
          el.okSender = false;
          el.sendError = true;
          if (el.loginError) {
            el.animError = true;
          }
          el.loginError = true;
        }
      );
    },
  },
};
</script>

<style>
.registration-btn {
  all: unset;
  color: rgb(255, 255, 255) !important;
  text-decoration: none;
  width: 100%;
}

.white-content.v-btn {
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
