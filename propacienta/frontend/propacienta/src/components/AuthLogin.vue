<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Авторизация</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-text-field
                prepend-icon="person"
                name="login"
                label="Адрес электронной почты"
                type="text"
                v-model="email"
              ></v-text-field>
              <v-text-field
                id="password"
                prepend-icon="lock"
                name="password"
                label="Пароль"
                type="password"
                v-model="password"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" v-on:click="onSubmit">Вход</v-btn>
            <v-btn color="primary" v-on:click="onMe">Me</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import request_service from "@/api/HTTP";
//import AUTH_REQUEST from "@/store/actions/auth";
export default {
  name: "AuthLogin",
  props: {
    source: String,
  },
  data: function () {
    return {
      email: null,
      password: null,
    };
  },
  methods: {
    onSubmit: function () {
      let data = {
        email: this.email,
        password: this.password,
      };
      this.$store.dispatch("AUTH_REQUEST", data);
    },
    onSubmxit: function () {
      let data = {
        email: this.email,
        password: this.password,
      };
      let config = {
        method: "post",
        url: "auth-token/",
        data: data,
      };
      request_service(
        config,
        function () {
          //console.log(...resp.headers);
          //console.log(resp.data);
        },
        function () {
          document.cookie =
            "csrftoken" + "=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
        }
        //
      );
    },
    onMe: function () {
      let config = {
        method: "get",
        url: "api/users/me",
      };
      request_service(
        config,
        function (resp) {
          console.log(resp.data);
          //alert(document.cookie);
        }
        //
      );
    },
  },
};
</script>

<style></style>
