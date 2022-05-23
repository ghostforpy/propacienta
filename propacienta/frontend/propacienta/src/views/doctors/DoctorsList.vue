<template>
  <div>
    <!-- <v-toolbar color="cyan" dark flat>
      <v-toolbar-title>Мои пациенты</v-toolbar-title>
    </v-toolbar> -->
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs10 sm8 md6>
          <v-row class="d-flex">
            <AppointmentOrder
              v-model="dialog"
              :doctorId="doctorId"
              :pacientId="$store.getters.pacient_id"
            >
            </AppointmentOrder>
            <v-col cols="12">
              <v-text-field
                v-model="searchDoctorQuery"
                color="cyan"
                placeholder="Введите Ф.И.О. или специальность"
                :loading="loading"
                :clearable="searchDoctorQuery != ''"
                append-icon="mdi-account-search-outline"
                @click:append="searchHandler"
                @keyup.enter="searchHandler"
                @keyup.delete="deleteHandler"
                @click:clear="clearHandler"
              ></v-text-field
            ></v-col>
            <template v-if="results.length > 0">
              <v-col
                cols="12"
                sm="6"
                lg="4"
                v-for="item in results"
                :key="item.id"
                class="py-2"
              >
                <router-link
                  class="doctor-card"
                  :to="{
                    name: 'doctor',
                    params: { doctorId: item.id },
                  }"
                >
                  <DoctorListCard
                    v-on:reserve="reserveHanlder"
                    :id="item.id"
                    :firstName="item.first_name"
                    :lastName="item.last_name"
                    :avatar="item.avatar"
                    :patronymic="item.patronymic"
                    :specializations="item.specializations"
                    :subSpecializations="item.sub_specializations"
                  ></DoctorListCard></router-link
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
            <!-- <v-col cols="12" v-else-if="!loading && searchDoctorQuery == ''">
              <v-card>
                <v-card-title class="text-h8 py-1">
                  У вас нет пациентов.
                </v-card-title>
              </v-card>
            </v-col> -->
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
import DoctorListCard from "@/components/doctors/DoctorListCard";
import AppointmentOrder from "@/components/appointments/AppointmentOrder";
export default {
  name: "DoctorsList",
  components: {
    DoctorListCard,
    AppointmentOrder,
  },
  data: function () {
    return {
      searchDoctorQuery: "",
      searchDoctorQueryOld: "",
      loading: false,
      nextPage: 1,
      emptyMyPacients: false,
      results: [],
      dialog: false,
      doctorId: 0,
    };
  },
  created: function () {
    this.loading = true;
    this.getDoctors();
    setTimeout(() => (this.loading = false), 1500);
  },
  methods: {
    deleteHandler: function () {
      if (this.searchDoctorQuery == "") {
        this.clearHandler();
      }
    },
    reserveHanlder: function (id) {
      // console.log(id);
      this.doctorId = id;
      this.dialog = true;
    },
    clearHandler: function () {
      this.loading = true;
      this.searchDoctorQuery = "";
      this.searchDoctorQueryOld = "";
      this.results = [];
      this.nextPage = 1;
      this.getDoctors();
      this.loading = false;
    },
    searchHandler: function () {
      this.loading = true;
      // setTimeout(() => (this.loading = true), 500);
      if (this.searchDoctorQuery != this.searchDoctorQueryOld) {
        this.nextPage = 1;
        this.searchDoctorQueryOld = this.searchDoctorQuery;
        this.results = [];
      }
      this.getDoctors();
      setTimeout(() => (this.loading = false), 500);
    },
    loadHandler: function () {
      this.loading = true;
      this.getDoctors();
      setTimeout(() => (this.loading = true), 500);
    },
    getDoctors: function () {
      if (this.nextPage == null) {
        return;
      }
      var el = this;
      let config = {
        method: "get",
        url: `api/doctors/`,
        params: {
          page: this.nextPage,
        },
      };
      // console.log(this.searchPacientQuery);
      if (this.searchDoctorQuery != "" && this.searchDoctorQuery != null) {
        config.params.search = this.searchDoctorQuery;
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
.doctor-card {
  text-decoration: none;
}
</style>
