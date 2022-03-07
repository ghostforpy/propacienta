<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="cyan darken-1">
            <v-toolbar-title>Регистрация</v-toolbar-title>
          </v-toolbar>
          <v-card-text v-if="!registrationSuccess">
            <v-form>
              <v-text-field
                name="email"
                label="Адрес электронной почты"
                type="text"
                v-model="email"
                ref="email"
                :rules="emailRules"
              ></v-text-field>
              <v-text-field
                name="phone_pacient"
                label="Телефон"
                type="text"
                v-model="phone_pacient"
                ref="phone_pacient"
                :rules="phoneRules"
              ></v-text-field>
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
              <v-checkbox
                v-model="role_doctor"
                label="Регистрация аккаунта врача"
              ></v-checkbox>
              <v-checkbox
                v-model="same_phone"
                v-if="role_doctor"
                label="Телефон соответствует основному"
              ></v-checkbox>
              <v-text-field
                v-show="role_doctor && !same_phone"
                name="phone_doctor"
                label="Телефон врача"
                type="text"
                v-model="phone_doctor"
                ref="phone_doctor"
                :rules="phoneRules"
              ></v-text-field>
            </v-form>
            <div v-if="registrationError" v-bind:class="{ shake: animError }">
              <v-alert transition="fade-transition" type="error">
                {{ errorsText }}
              </v-alert>
            </div>
          </v-card-text>
          <v-card-text v-else>
            Вам на электронную почту отправлено письмо с ссылкой для активации
            аккаунта. <br />Для завершения регистрации перейдите по ссылке в
            полученном электронном письме.
            <span v-if="role_doctor"
              ><br />Активация аккаунта с полномочиями "Доктор" осуществляется
              администратором сервиса.</span
            >
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              block
              color="cyan"
              class="white-content"
              v-on:click="onSubmit"
              v-if="!registrationSuccess"
              ><span v-if="!loading">Зарегистрироваться</span
              ><v-progress-circular
                v-else
                indeterminate
                color="primary"
              ></v-progress-circular
            ></v-btn>
            <v-btn color="cyan" class="white-content" v-on:click="onOk" v-else
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
      phone_pacient: null,
      password: null,
      re_password: null,
      role_doctor: false,
      registrationSuccess: false,
      registrationError: false,
      animError: false,
      loading: false,
      phone_doctor: null,
      same_phone: false,
      submitAvailableSt: false,
      phoneRules: [
        (value) => !!value || "Это поле является обязательным.",
        (value) => {
          const pattern = /^[+]*[0-9]{11}$/g;
          return pattern.test(value) || "Неправильный формат номера.";
        },
      ],
      emailRules: [
        (value) => !!value || "Это поле является обязательным.",
        (value) => {
          const pattern =
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return pattern.test(value) || "Неправильный формат номера.";
        },
      ],
    };
  },
  computed: {
    errorsText: function () {
      if (this.password != this.re_password) {
        return "Два пароля не совпадают.";
      }
      return `${this.$store.getters.registrationErrorState} ${this.$store.getters.registrationErrorEmailState} 
      ${this.$store.getters.registrationErrorPasswordState} ${this.$store.getters.registrationErrorPhoneState}`;
    },
  },
  methods: {
    onOk: function () {
      this.$router.push({
        path: "/",
      });
    },
    submitAvailable: function () {
      return (
        this.email != null &&
        this.password != null &&
        this.re_password != null &&
        this.phone_pacient != null &&
        this.$refs.email.valid &&
        this.$refs.password.valid &&
        this.$refs.re_password.valid &&
        this.$refs.phone_pacient.valid &&
        this.password === this.re_password &&
        !(
          this.role_doctor &&
          !this.same_phone &&
          !this.$refs.phone_doctor.valid
        )
      );
    },
    onSubmit: async function () {
      if (!this.submitAvailable()) {
        if (this.registrationError) {
          this.animError = true;
        }
        this.registrationError = true;
        return;
      }
      if (this.password != this.re_password) {
        if (this.registrationError) {
          this.animError = true;
        }
        this.registrationError = true;
        return;
      }
      let data = {
        email: this.email,
        phone_pacient: this.phone_pacient,
        password: this.password,
        re_password: this.re_password,
        role_doctor: this.role_doctor,
        phone_doctor:
          this.role_doctor && this.same_phone
            ? this.phone_pacient
            : this.phone_doctor,
      };
      this.animError = false;
      this.loading = true;
      const res = await this.$store.dispatch(REGISTRATION_REQUEST, data);
      this.loading = false;
      if (res) {
        this.registrationError = false;
        this.registrationSuccess = true;
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
