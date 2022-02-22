<!-- App.vue -->
<template>
  <v-app>
    <v-app-bar color="cyan accent-4" dark absolute>
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="d-block d-md-none"
      ></v-app-bar-nav-icon>
      <v-row justify="space-between" no-gutters class="nav-bar-header">
        <v-toolbar-title
          ><router-link to="/" class="text-decoration-none"
            ><v-btn icon> <v-icon>mdi-medical-bag</v-icon></v-btn
            >Propacienta</router-link
          >
        </v-toolbar-title>
        <v-toolbar-title class="d-none d-md-block"
          ><router-link to="/appointment"
            ><v-btn icon> <v-icon>mdi-calendar-month</v-icon></v-btn
            >Приёмы</router-link
          >
        </v-toolbar-title>
        <v-toolbar-title class="d-none d-md-block"
          ><router-link to="/hospitals"
            ><v-btn icon> <v-icon>mdi-hospital-building</v-icon></v-btn
            >Клиники</router-link
          >
        </v-toolbar-title>
        <v-toolbar-title class="d-none d-md-block"
          ><router-link to="/doctors">
            <v-btn icon> <v-icon>mdi-doctor</v-icon></v-btn
            >Врачи</router-link
          >
        </v-toolbar-title>
      </v-row>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>

      <v-menu bottom transition="slide-y-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-btn dark icon v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>

        <v-list class="account-menu">
          <v-list-item
            dense="true"
            v-for="(item, i) in accountMenuList"
            :key="i"
          >
            <router-link :to="item.route"> {{ item.title }}</router-link>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item>
            <router-link to="/logout">Выход</router-link>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary
      class="nav-bar-drawer"
    >
      <v-list nav dense>
        <v-list-item-group
          v-model="group"
          active-class="deep-purple--text text--accent-4"
        >
          <v-list-item>
            <v-list-item-title
              ><router-link to="/medicine-card"
                ><v-btn icon>
                  <v-icon>mdi-card-account-details-outline</v-icon></v-btn
                >Медицинская карта</router-link
              ></v-list-item-title
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title
              ><router-link to="/appointment"
                ><v-btn icon> <v-icon>mdi-calendar-month</v-icon></v-btn
                >Приёмы</router-link
              ></v-list-item-title
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title
              ><router-link to="/hospitals"
                ><v-btn icon> <v-icon>mdi-hospital-building</v-icon></v-btn
                >Клиники</router-link
              ></v-list-item-title
            >
          </v-list-item>

          <v-list-item>
            <v-list-item-title
              ><router-link to="/doctors">
                <v-btn icon> <v-icon>mdi-doctor</v-icon></v-btn
                >Врачи</router-link
              ></v-list-item-title
            >
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view></router-view>
    </v-main>

    <v-footer color="cyan lighten-1" padless>
      <v-row justify="center" no-gutters>
        <v-btn
          v-for="link in links"
          :key="link"
          color="white"
          text
          rounded
          class="my-2"
        >
          {{ link }}
        </v-btn>
        <v-col class="cyan lighten-2 py-4 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>
<script>
import { AUTH_PING } from "@/store/actions/auth";
export default {
  name: "App",
  data: () => ({
    drawer: false,
    group: null,
    links: ["Home", "About Us", "Team", "Services", "Blog", "Contact Us"],
    accountMenuList: [
      { title: "Медицинская карта", route: "/my-medicine-card" },
      { title: "Мой профиль", route: "/my-profile" },
    ],
  }),
  watch: {
    group() {
      this.drawer = false;
    },
  },
  created: function () {
    var path = this.$route.path;
    this.$store.dispatch(AUTH_PING).then(() => {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push(path);
      }
    });
  },
};
</script>
<style>
.nav-bar-header a {
  all: unset;
  color: rgb(255, 255, 255) !important;
  text-decoration: none;
}
.nav-bar-drawer a {
  all: unset;
  color: rgb(83, 83, 83) !important;
  text-decoration: none;
}
.account-menu a {
  all: unset;
  color: rgb(83, 83, 83) !important;
  text-decoration: none;
}
</style>