<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="cyan darken-1">
            <v-toolbar-title>Авторизация</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-text-field
                prepend-icon="mdi-email"
                name="login"
                label="Адрес электронной почты"
                type="text"
                v-model="email"
              ></v-text-field>
              <v-text-field
                id="password"
                prepend-icon="mdi-lock"
                name="password"
                label="Пароль"
                type="password"
                v-model="password"
              ></v-text-field>
            </v-form>
            <v-flex class="caption text-xs-right"
              ><router-link to="/recover-password"
                >Забыли пароль?</router-link
              ></v-flex
            >
            <div v-if="loginError" v-bind:class="{ shake: animError }">
              <v-alert transition="fade-transition" type="error">
                {{ loginErrorText }}
              </v-alert>
            </div>
          </v-card-text>
          <v-card-actions>
            <router-link
              :to="{ name: 'registration' }"
              block
              class="registration-btn"
              ><v-btn color="light-blue"> Регистрация</v-btn></router-link
            >
            <v-spacer></v-spacer>
            <v-btn color="cyan" v-on:click="onSubmit">Вход</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { AUTH_REQUEST } from "@/store/actions/auth";
export default {
  name: "AuthLogin",
  props: {
    source: String,
  },
  data: function () {
    return {
      email: null,
      password: null,
      loginError: false,
      animError: false,
    };
  },
  computed: {
    // loginError: function () {
    //   return this.$store.getters.authErrorStatus != 0;
    // },
    loginErrorText: function () {
      if (this.loginError) {
        if (this.$store.getters.authErrorStatus == 400) {
          return "Неверный логин или пароль";
        }
      }
      return "Сервер недоступен";
    },
  },
  methods: {
    onSubmit: async function () {
      let data = {
        email: this.email,
        password: this.password,
      };
      this.animError = false;
      const res = await this.$store.dispatch(AUTH_REQUEST, data);
      if (res) {
        this.loginError = false;
        const path =
          this.$route.query.redirect != undefined
            ? this.$route.query.redirect
            : "/";
        this.$router.push({
          path: path,
        });
      } else {
        if (this.loginError) {
          this.animError = true;
        }
        this.loginError = true;
      }
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
