<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="cyan darken-1">
            <v-toolbar-title>Регистрация</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-text-field
                name="email"
                label="Адрес электронной почты"
                type="text"
                v-model="email"
              ></v-text-field>
              <v-text-field
                id="password"
                name="password"
                label="Пароль"
                type="password"
                v-model="password"
              ></v-text-field>
              <v-text-field
                id="re_password"
                name="re_password"
                label="Повторите пароль"
                type="password"
                v-model="re_password"
              ></v-text-field>
              <v-checkbox
                v-model="role_doctor"
                label="Регистрация аккаунта врача"
              ></v-checkbox>
              <!-- <v-text-field
                name="first_name"
                label="Имя"
                type="text"
                v-model="first_name"
              ></v-text-field>
              <v-text-field
                name="last_name"
                label="Фамилия"
                type="text"
                v-model="last_name"
              ></v-text-field> -->
            </v-form>
            <div v-if="registrationError" v-bind:class="{ shake: animError }">
              <v-alert transition="fade-transition" type="error">
                {{ errorsText }}
              </v-alert>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="cyan" v-on:click="onSubmit">Зарегистрироваться</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import {
  // REGISTRATION_ERROR,
  REGISTRATION_REQUEST,
  // REGISTRATION_SUCCESS,
} from "@/store/actions/registration";
export default {
  name: "RegistrationView",
  props: {
    source: String,
  },
  data: function () {
    return {
      email: null,
      password: null,
      re_password: null,
      role_doctor: false,

      registrationError: false,
      animError: false,
    };
  },
  computed: {
    errorsText: function () {
      return `${this.$store.getters.registrationErrorEmailState} ${this.$store.getters.registrationErrorPasswordState}`;
    },
  },
  methods: {
    onSubmit: async function () {
      let data = {
        email: this.email,
        password: this.password,
        re_password: this.re_password,
        role_doctor: this.role_doctor,
      };
      this.animError = false;

      const res = await this.$store.dispatch(REGISTRATION_REQUEST, data);

      if (res) {
        this.registrationError = false;
        // const path =
        //   this.$route.query.redirect != undefined
        //     ? this.$route.query.redirect
        //     : "/";
        // this.$router.push({
        //   path: path,
        // });
      } else {
        if (this.registrationError) {
          this.animError = true;
        }
        this.registrationError = true;
      }
    },
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
