<!-- App.vue -->
<template>
  <v-app>
    <v-app-bar color="cyan accent-4" dark absolute app>
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

      <v-menu
        bottom
        transition="slide-y-transition"
        v-if="isAuthenticated"
        :close-on-content-click="false"
        v-model="menu"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn dark icon v-bind="attrs" v-on="on">
            <v-icon>{{ accountIcon }}</v-icon>
          </v-btn>
        </template>

        <v-list class="account-menu">
          <v-list-item
            dense
            v-for="(item, i) in accountMenuList"
            :key="i"
            @click="menu = false"
          >
            <router-link :to="item.route"> {{ item.title }}</router-link>
          </v-list-item>
          <v-divider v-if="docModeAvailable"></v-divider>
          <v-list-item v-if="docModeAvailable">
            <v-list-item-action
              ><v-switch
                color="cyan"
                v-model="docMode"
                inset
                label="Режим врача"
                @click="clickSwitcherDocMode"
              ></v-switch
            ></v-list-item-action>
          </v-list-item>
          <v-list-item v-if="docMode" dense @click="menu = false">
            <router-link :to="{ name: 'my-doctor-profile' }">
              Мой профиль врача</router-link
            >
          </v-list-item>
          <v-list-item v-if="docMode" dense @click="menu = false">
            <router-link :to="{ name: 'my-pacients' }">
              Мои пациенты</router-link
            >
          </v-list-item>
          <v-list-item v-if="docMode" dense @click="menu = false">
            <router-link :to="{ name: 'main' }"> Мой календарь</router-link>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="menu = false">
            <router-link to="/logout">Выход</router-link>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn icon v-else>
        <v-icon @click="$router.push('/login')">mdi-lock</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary
      class="nav-bar-drawer"
      app
    >
      <v-list nav dense>
        <v-list-item-group
          v-model="group"
          active-class="deep-purple--text text--accent-4"
        >
          <v-list-item v-for="(link, id) in computedDrawerMenuList" :key="id">
            <v-list-item-title
              ><router-link :to="link.route"
                ><v-btn icon>
                  <v-icon class="nav-bar-drawer-icon">{{
                    link.icon
                  }}</v-icon></v-btn
                >{{ link.title }}</router-link
              ></v-list-item-title
            >
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view></router-view>
    </v-main>

    <v-footer color="cyan lighten-1" padless app :absolute="true">
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
          {{ new Date().getFullYear() }} — <strong>Propacienta</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>
<script>
import { AUTH_PING } from "@/store/actions/auth";
import { TOOGLE_DOC_MODE } from "@/store/actions/user";

export default {
  name: "App",
  data: () => ({
    docMode: false,
    // docModeAvailable: false,
    menu: false,
    drawer: false,
    group: null,
    links: ["Home", "About Us", "Team", "Services", "Blog", "Contact Us"],
    accountMenuList: [
      { title: "Медицинская карта", route: "/my-medicine-card" },
      { title: "Мой профиль", route: "/users/me" },
    ],
    drawerMenuList: [
      {
        title: "Медицинская карта",
        route: "/my-medicine-card",
        icon: "mdi-card-account-details-outline",
        needAuth: true,
      },
      {
        title: "Приёмы",
        route: "/appointment",
        icon: "mdi-calendar-month",
        needAuth: false,
      },
      {
        title: "Клиники",
        route: "/hospitals",
        icon: "mdi-hospital-building",
        needAuth: false,
      },
      {
        title: "Врачи",
        route: "/doctors",
        icon: "mdi-doctor",
        needAuth: false,
      },
    ],
  }),
  watch: {
    group() {
      this.drawer = false;
    },
  },
  beforeCreate: async function () {
    await this.$store.dispatch(AUTH_PING);
    this.docMode = this.$store.getters.docMode;
  },
  methods: {
    clickSwitcherDocMode: async function () {
      await this.$store.dispatch(TOOGLE_DOC_MODE, this.docMode);
    },
  },
  computed: {
    docModeAvailable: function () {
      return this.$store.getters.docModeAvailable;
    },
    accountIcon: function () {
      return !this.docMode ? "mdi-account" : "mdi-doctor";
    },
    isAuthenticated: function () {
      return this.$store.getters.isAuthenticated;
    },
    computedDrawerMenuList: function () {
      return this.drawerMenuList.filter(
        (item) =>
          this.isAuthenticated || (!this.isAuthenticated && !item.needAuth)
      );
    },
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
.nav-bar-drawer-icon {
  color: rgb(83, 83, 83) !important;
}
.account-menu a {
  all: unset;
  color: rgb(83, 83, 83) !important;
  text-decoration: none;
}
</style>