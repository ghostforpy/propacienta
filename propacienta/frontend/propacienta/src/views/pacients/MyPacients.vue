<template>
  <div>
    <v-toolbar color="cyan" dark flat>
      <v-toolbar-title>Мои пациенты</v-toolbar-title>
    </v-toolbar>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs10 sm8 md6>
          <v-row>
            <AppointmentOrder
              v-model="dialog"
              :doctorId="$store.getters.doctor_id"
              :pacientId="pacientId"
              :docMode="true"
            >
            </AppointmentOrder>
            <v-col cols="12">
              <v-text-field
                v-model="searchPacientQuery"
                color="cyan"
                placeholder="Введите Ф.И.О. или номер телефона"
                :loading="loading"
                :clearable="searchPacientQuery != ''"
                append-icon="mdi-account-search-outline"
                @click:append="searchHandler"
                @keyup.enter="searchHandler"
                @click:clear="clearHandler"
                @keyup.delete="deleteHandler"
              ></v-text-field
            ></v-col>
            <template v-if="results.length > 0">
              <v-col
                cols="12"
                v-for="item in results"
                :key="item.id"
                class="py-2"
              >
                <router-link
                  class="pacient-card"
                  :to="{
                    name: 'pacient-medicine-card',
                    params: { pacientId: item.id },
                  }"
                >
                  <PacientListCard
                    :id="item.id"
                    v-on:reserve="reserveHanlder"
                    :firstName="item.first_name"
                    :lastName="item.last_name"
                    :patronymic="item.patronymic"
                    :birthday="item.birthday"
                  ></PacientListCard></router-link
              ></v-col>
              <v-col cols="12" class="d-flex justify-center">
                <v-btn
                  v-if="nextPage != null"
                  class="ma-2 white-content"
                  :loading="loading"
                  :disabled="loading"
                  color="cyan lighten-3"
                  rounded
                  @click="loadHandler"
                >
                  Ещё
                </v-btn>
              </v-col>
            </template>
            <v-col cols="12" v-else-if="!loading && searchPacientQuery == ''">
              <v-card>
                <v-card-title class="text-h8 py-1">
                  У вас нет пациентов.
                </v-card-title>
              </v-card>
            </v-col>
            <v-col cols="12" v-else-if="!loading">
              <v-card>
                <v-card-title class="text-h8 py-1">
                  По вашему запросу ничего не найдено.
                </v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </v-flex></v-layout
      >
    </v-container>
  </div>
</template>

<script>
import request_service from "@/api/HTTP";
import PacientListCard from "@/components/pacients/PacientListCard";
import AppointmentOrder from "@/components/appointments/AppointmentOrder";
export default {
  name: "MyPacients",
  components: {
    PacientListCard,
    AppointmentOrder,
  },
  data: function () {
    return {
      searchPacientQuery: "",
      searchPacientQueryOld: "",
      loading: false,
      nextPage: 1,
      emptyMyPacients: false,
      results: [],
      dialog: false,
      pacientId: 0,
    };
  },
  created: function () {
    this.loading = true;
    this.getPacients();
    setTimeout(() => (this.loading = false), 500);
  },
  methods: {
    reserveHanlder: function (id) {
      // console.log(id);
      this.pacientId = id;
      this.dialog = true;
    },
    deleteHandler: function () {
      if (this.searchPacientQuery == "") {
        this.clearHandler();
      }
    },
    clearHandler: function () {
      this.loading = true;
      this.searchPacientQuery = "";
      this.searchPacientQueryOld = "";
      this.results = [];
      this.nextPage = 1;
      this.getPacients();
      this.loading = false;
    },
    // loadPacients: function () {
    //   this.loading = !this.loading;
    // },
    searchHandler: function () {
      this.loading = true;
      // setTimeout(() => (this.loading = true), 500);
      if (this.searchPacientQuery != this.searchPacientQueryOld) {
        this.nextPage = 1;
        this.searchPacientQueryOld = this.searchPacientQuery;
        this.results = [];
      }
      this.getPacients();
      setTimeout(() => (this.loading = false), 500);
    },
    loadHandler: function () {
      this.loading = true;
      this.getPacients();
      setTimeout(() => (this.loading = true), 500);
    },
    getPacients: function () {
      if (this.nextPage == null) {
        return;
      }
      var el = this;
      let config = {
        method: "get",
        url: `api/pacients/`,
        params: {
          page: this.nextPage,
        },
        headers: { IsDoctor: true },
      };
      // console.log(this.searchPacientQuery);
      if (this.searchPacientQuery != "" && this.searchPacientQuery != null) {
        config.params.search = this.searchPacientQuery;
        config.params.page = this.nextPage;
      }
      request_service(
        config,
        function (resp) {
          let r = resp.data.results;
          el.results.push(...r);
          if (resp.data.next != null) {
            let nextUrl = new URL(resp.data.next);
            el.nextPage = nextUrl.searchParams.get("page");
          } else {
            el.nextPage = null;
          }
        },
        function (error) {
          console.log(error.response);
        }
      );
    },
  },
};
</script>

<style>
.pacient-card {
  text-decoration: none;
}
</style>
