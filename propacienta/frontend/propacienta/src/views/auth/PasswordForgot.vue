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
                prepend-icon="mdi-email"
                name="login"
                label="Адрес электронной почты"
                type="text"
                v-model="email"
                :rules="[
                  (value) => !!value || 'Это поле является обязательным.',
                ]"
                ref="email"
              ></v-text-field>
            </v-form>
            <div v-if="sendError" v-bind:class="{ shake: animError }">
              <v-alert transition="fade-transition" type="error">
                {{ sendErrorText }}
              </v-alert>
            </div>
          </v-card-text>
          <v-card-text v-else>
            Вам на электронную почту отправлено письмо со ссылкой для сброса
            пароля. Для завершения перейдите по ссылке в полученном электронном
            письме.
          </v-card-text>
          <v-card-actions>
            <v-btn
              class="white-content"
              color="cyan"
              v-on:click="onSubmit"
              v-if="!okSender"
              block
              >Сбросить</v-btn
            >
            <v-btn
              class="white-content"
              color="cyan"
              :to="{ name: 'main' }"
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
  name: "PasswordForgot",
  props: {
    source: String,
  },
  data: function () {
    return {
      email: null,
      okSender: false,
      animError: false,
      sendError: false,
      sendErrorText: "Что-то пошло не так. Попробуйте позже.",
    };
  },
  mounted: function () {
    const recaptcha = this.$recaptchaInstance;
    recaptcha.showBadge();
  },
  beforeDestroy: function () {
    const recaptcha = this.$recaptchaInstance;
    recaptcha.hideBadge();
  },
  methods: {
    emailValidate: function () {
      const pattern =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      if (!pattern.test(this.email)) {
        this.$refs.email.valid = false;
        this.$refs.email.errorBucket.push("Неправильный формат адреса.");
        return false;
      }
      return true;
    },
    onSubmit: async function () {
      if (!this.emailValidate()) {
        return;
      }
      var data = {
        email: this.email,
        // password: this.password,
      };
      if (process.env.NODE_ENV === "production") {
        await this.$recaptchaLoaded();
        const token = await this.$recaptcha("login");
        if (!token) {
          return;
        }
        data.recaptchatoken = token;
      }
      let config = {
        method: "post",
        url: `api/users/reset_password/`,
        data: data,
      };
      var el = this;
      this.animError = false;
      request_service(
        config,
        function (resp) {
          console.log(resp);
          el.okSender = true;
          el.sendError = false;
        },
        function (error) {
          console.log(error);
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
