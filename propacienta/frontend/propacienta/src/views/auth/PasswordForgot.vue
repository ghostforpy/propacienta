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
// import { AUTH_REQUEST, AUTH_PING } from "@/store/actions/auth";
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
  computed: {
    // loginError: function () {
    //   return this.$store.getters.authErrorStatus != 0;
    // },
    // loginErrorText: function () {
    //   if (this.loginError) {
    //     if (this.$store.getters.authErrorStatus == 400) {
    //       return "Неверный логин или пароль";
    //     }
    //   }
    //   return "Сервер недоступен";
    // },
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
      let data = {
        email: this.email,
        // password: this.password,
      };
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
          // el.docModeError = false;
          // // console.log(resp);
          // el.firstName = resp.data.first_name;
          // el.lastName = resp.data.last_name;
          // el.patronymic = resp.data.patronymic;
          // el.medicineCardId = resp.data.medicinecard;
          // el.birthday = resp.data.birthday;
          // el.phone = resp.data.phone;
        },
        function (error) {
          console.log(error);
          el.okSender = false;
          el.sendError = true;
          if (el.loginError) {
            el.animError = true;
          }
          el.loginError = true;

          // el.docModeError = true;
          // if (error.response.status == 404) {
          //   el.$router.push({ name: "notfound" });
          //   return;
          // }
          // if (error.response.status == 403) {
          //   el.docModeError = true;
          //   el.errorToolbarText =
          //     "Вы не являетесь лечащим врачом данного пациента.";
          //   return;
          // }
          // el.$router.push({ name: "main" });
        }
      );

      // this.animError = false;
      // const res = await this.$store.dispatch(AUTH_REQUEST, data);
      // if (res) {
      //   await this.$store.dispatch(AUTH_PING);
      //   this.loginError = false;
      //   const path =
      //     this.$route.query.redirect != undefined
      //       ? this.$route.query.redirect
      //       : "/";
      //   this.$router.push({
      //     path: path,
      //   });
      // } else {
      //   if (this.loginError) {
      //     this.animError = true;
      //   }
      //   this.loginError = true;
      // }
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
