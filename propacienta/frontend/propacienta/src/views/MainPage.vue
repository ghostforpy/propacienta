<template>
  <v-container fluid fill-height class="cyan lighten-5">
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md8>
        <v-row>
          <template v-for="(item, id) in firstTabs">
            <v-col
              :key="id"
              cols="6"
              md="4"
              v-bind:class="[
                !((id + 1) % 3) ? dNoneClass : '',
                dMdBlockClass,
                mainPageColClass,
              ]"
            >
              <v-img contain max-height="100" :src="item.src"></v-img>
              <p
                class="
                  tabs-text
                  font-weight-bold
                  text-center
                  teal--text
                  text--lighten-2
                "
              >
                {{ item.text }}
              </p>
            </v-col>
          </template>
        </v-row>
        <v-row>
          <v-col>
            <p class="teal--text text--darken-2 center-text-class text-center">
              Твоя медицинская карта из любой точки мира
            </p>
            <p
              class="
                teal--text
                text--darken-2
                center-pacients-text-class
                text-center
              "
            >
              Нам доверяют {{ pacientsNumber }} {{ skloneniePacients }}.
            </p>
            <p
              class="
                teal--text
                text--darken-2
                center-pacients-text-class
                text-center
              "
            >
              У нас работает {{ doctorsNumber }} {{ sklonenieDoctors }}.
            </p>
          </v-col>
        </v-row>
        <v-row>
          <template v-for="(item, id) in secondTabs">
            <v-col
              :key="id"
              cols="6"
              md="4"
              v-bind:class="[
                !((id + 1) % 3) ? dNoneClass : '',
                dMdBlockClass,
                mainPageColClass,
              ]"
            >
              <v-img contain max-height="100" :src="item.src"></v-img>
              <p
                class="
                  tabs-text
                  font-weight-bold
                  text-center
                  teal--text
                  text--lighten-2
                "
              >
                {{ item.text }}
              </p>
            </v-col>
          </template>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
function sclonenie(number, txt) {
  const cases = [2, 0, 1, 1, 1, 2];
  return txt[
    number % 100 > 4 && number % 100 < 20
      ? 2
      : cases[number % 10 < 5 ? number % 10 : 5]
  ];
}
import request_service from "@/api/HTTP";

export default {
  name: "MainPage",
  data: () => ({
    mainPageColClass: "main_page__col",
    dNoneClass: "d-none",
    dMdBlockClass: "d-md-block",
    pacientsNumber: Math.floor(Math.random() * (1000 - 100 + 1)) + 100,
    doctorsNumber: Math.floor(Math.random() * (1000 - 100 + 1)) + 100,
    firstTabs: [
      {
        text: "Твои анализы",
        src: require("@/assets/main_page/cones1.png"),
      },
      {
        text: "Твои антропометрические данные (рост, вес)",
        src: require("@/assets/main_page/tape1.png"),
      },
      {
        text: "Твои результаты КТ, МРТ и рентген исследований",
        src: require("@/assets/main_page/edges1.png"),
      },
    ],
    secondTabs: [
      {
        text: "Твои анализы",
        src: require("@/assets/main_page/cones1.png"),
      },
      {
        text: "Твои антропометрические данные (рост, вес)",
        src: require("@/assets/main_page/tape1.png"),
      },
      {
        text: "Твои результаты КТ, МРТ и рентген исследований",
        src: require("@/assets/main_page/edges1.png"),
      },
    ],
  }),
  mounted: async function () {
    let config = {
      method: "get",
      url: `api/doctors/doctors-count/`,
    };
    var el = this;
    request_service(
      config,
      function (resp) {
        // console.log(resp);
        el.doctorsNumber = resp.data.doctors_count;
      },
      function () {}
    );
    config = {
      method: "get",
      url: `api/pacients/pacients-count/`,
    };
    request_service(
      config,
      function (resp) {
        // console.log(resp);
        el.pacientsNumber = resp.data.pacients_count;
      },
      function () {}
    );
  },
  computed: {
    conesImg: function () {
      return require("@/assets/main_page/cones1.png");
    },
    skloneniePacients: function () {
      const number = this.pacientsNumber;
      const txt = ["пациент", "пациента", "пациентов"];
      return sclonenie(number, txt);
    },
    sklonenieDoctors: function () {
      const number = this.doctorsNumber;
      const txt = ["врач", "врача", "врачей"]; //проверить
      return sclonenie(number, txt);
    },
    tapeImg: function () {
      return require("@/assets/main_page/tape1.png");
    },
    edgesImg: function () {
      return require("@/assets/main_page/edges1.png");
    },
  },
};
</script>

<style>
.main_page__col {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.tabs-text {
  font-family: serif;
  font-size: 1.25rem !important;
  font-weight: 500;
  line-height: 2rem;
  letter-spacing: 0.0125em !important;
  overflow-wrap: break-word;
}
.center-text-class {
  font-family: serif;
  font-size: 3rem !important;
  font-weight: 400;
  line-height: 3.125rem;
  letter-spacing: normal !important;
}
.center-pacients-text-class {
  font-family: serif;
  font-size: 1.75rem !important;
  font-weight: 300;
  line-height: 2.125rem;
  letter-spacing: normal !important;
}
</style>
