<!-- App.vue -->
<template>
  <v-app>
    <v-app-bar app color="blue">
      <v-app-bar-title>
        <h3 class="text-h4 white--text">Propacienta</h3>
      </v-app-bar-title>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>
<script>
//import AUTH_PING from "@/store/actions/auth";
export default {
  name: "App",
  created: function () {
    this.$store.dispatch("AUTH_PING").then(() => {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push("/");
      }
    });
  },
};
</script>