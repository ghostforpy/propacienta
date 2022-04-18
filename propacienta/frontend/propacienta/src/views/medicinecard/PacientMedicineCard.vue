<template>
  <div v-if="!docModeError">
    <v-toolbar color="cyan" dark flat>
      <v-toolbar-title>Медицинская карта</v-toolbar-title>
    </v-toolbar>
    <v-tabs background-color="cyan" dark show-arrows centered>
      <v-tabs-slider color="yellow"></v-tabs-slider>
      <v-tab href="#common-data" @click="handleClickTab">Общие данные</v-tab>
      <v-tab href="#research" @click="handleClickTab">Исследования</v-tab>
      <v-tab href="#analisis" @click="handleClickTab">Анализы</v-tab>
      <v-tab href="#transfered-diseases" @click="handleClickTab"
        >Перенесенные заболевания</v-tab
      >
      <v-tab href="#chronic-diseases" @click="handleClickTab"
        >Хронические заболевания</v-tab
      >
      <v-tab-item id="common-data">
        <CommonDataMedicineCardDoctor
          :pacientId="pacientId"
          :medicineCard="medicineCardId"
          :firstName="firstName"
          :lastName="lastName"
          :patronymic="patronymic"
          :birthday="birthday"
          :phone="phone"
        >
        </CommonDataMedicineCardDoctor>
      </v-tab-item>
      <v-tab-item id="research">
        <OwnerMedicineIndependentResearch
          :pacientId="pacientId"
          :medicineCard="medicineCardId"
        >
        </OwnerMedicineIndependentResearch>
      </v-tab-item>
      <v-tab-item id="analisis">
        <OwnerAnalisys :pacientId="pacientId" :medicineCard="medicineCardId">
        </OwnerAnalisys>
      </v-tab-item>
      <v-tab-item id="transfered-diseases">
        <OwnerTransferedDiseases
          :pacientId="pacientId"
          :medicineCard="medicineCardId"
        >
        </OwnerTransferedDiseases>
      </v-tab-item>
      <v-tab-item id="chronic-diseases">
        <OwnerChronicDiseases :pacientId="pacientId"> </OwnerChronicDiseases>
      </v-tab-item>
    </v-tabs>
  </div>
  <v-container align-center justify-center v-else fill-height fluid>
    <v-flex xs12 sm8 md6>
      <v-card class="elevation-12">
        <v-toolbar dark color="cyan darken-1">
          <v-toolbar-title>{{ errorToolbarTitle }}</v-toolbar-title>
        </v-toolbar>
        <v-card-text>{{ errorToolbarText }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="cyan" class="white-content" v-on:click="$router.go(-1)"
            >Ok</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-container>
</template>

<script>
import request_service from "@/api/HTTP";
import CommonDataMedicineCardDoctor from "@/components/medicinecard/CommonDataMedicineCardDoctor";
import OwnerMedicineIndependentResearch from "@/components/medicinecard/IndependentResearch";
import OwnerAnalisys from "@/components/medicinecard/OwnerAnalisys";
import OwnerTransferedDiseases from "@/components/medicinecard/OwnerTransferedDiseases";
import OwnerChronicDiseases from "@/components/medicinecard/OwnerChronicDiseases";
// import { INIT_PACIENT_STATE } from "@/store/actions/pacient";
// import DateFieldUserOwner from "@/components/users/DateFieldUserOwner";
// import { USER_REQUEST } from "@/store/actions/user";
export default {
  name: "PacientMedicineCard",
  props: {
    source: String,
  },
  components: {
    CommonDataMedicineCardDoctor,
    OwnerMedicineIndependentResearch,
    OwnerAnalisys,
    OwnerTransferedDiseases,
    OwnerChronicDiseases,
  },
  data: function () {
    return {
      page: "",
      docModeError: false,
      errorToolbarTitle: "В доступе отказано",
      errorToolbarText: 'Для доступа требуется активировать режим "Врач".',
      firstName: undefined,
      lastName: undefined,
      patronymic: undefined,
      medicineCardId: undefined,
      birthday: undefined,
      phone: undefined,
      //   height: "",
      //   weight: "",
      //   applyBtn: false,
      //   loading: false,
      //   // numberRules: [(value) => !!value || "Это поле является обязательным."],
      //   numberRules: [
      //     (value) => !!value || "Это поле является обязательным.",
      //     (value) => {
      //       const pattern = /^[1-2]?\d\d([.,]\d\d?)?$/g;
      //       return pattern.test(value) || "Неправильный формат.";
      //     },
      //   ],
    };
  },
  mounted: async function () {
    if (!this.$store.getters.docMode) {
      this.docModeError = true;
    } else {
      this.docModeError = false;
      let config = {
        method: "get",
        url: `api/pacients/${this.pacientId}/`,
        headers: {
          IsDoctor: true,
        },
      };
      var el = this;
      request_service(
        config,
        function (resp) {
          el.docModeError = false;
          // console.log(resp);
          el.firstName = resp.data.first_name;
          el.lastName = resp.data.last_name;
          el.patronymic = resp.data.patronymic;
          el.medicineCardId = resp.data.medicinecard;
          el.birthday = resp.data.birthday;
          el.phone = resp.data.phone;
        },
        function (error) {
          console.log(error);
          console.log(error.response);
          el.docModeError = true;
          if (error.response.status == 404) {
            console.log(404);
            el.$router.push({ name: "notfound" });
            return;
          }
          if (error.response.status == 403) {
            el.docModeError = true;
            el.errorToolbarText =
              "Вы не являетесь лечащим врачом данного пациента.";
            return;
          }
          el.$router.push({ name: "main" });
        }
      );
    }
    if (this.$route.hash != "") {
      this.page = this.$route.hash.replace("#", "");
    }
  },
  computed: {
    pacientId: function () {
      return parseInt(this.$route.params.pacientId);
      // return this.$store.getters.pacient_id;
    },
    //     pacientId: function () {
    //   return parseInt(this.$route.params.pacientId);
    //   // return this.$store.getters.pacient_id;
    // },
    // submitAvailable: function () {
    //   const v =
    //     this.height != null &&
    //     this.height != "" &&
    //     this.weight != null &&
    //     this.weight != "";
    //   return v;
    // },
  },
  methods: {
    handleClickTab: function (event) {
      var hash = event.target.hash;
      if (this.$route.hash != hash) {
        this.$router.replace({
          name: this.$route.name,
          hash: hash,
          params: { pacientId: this.$route.params.pacientId },
        });
      }
    },
    // updateHandl: function () {
    // if (
    //   this.first_name != this.$store.state.user.first_name ||
    //   this.last_name != this.$store.state.user.last_name ||
    //   this.patronymic != this.$store.state.user.patronymic ||
    //   this.pacient_phone != this.$store.state.user.pacient_phone ||
    //   this.birthday.toISOString().substr(0, 10) !=
    //     new Date(this.$store.state.user.birthday).toISOString().substr(0, 10)
    // ) {
    //   this.applyBtn = true;
    // } else {
    //   this.applyBtn = false;
    // }
  },
  //   onSubmit: async function () {
  //     if (!this.$refs.pacient_phone.$refs.field.valid) {
  //       return;
  //     }
  //     this.loading = true;
  //     let data = {
  //       first_name: this.first_name,
  //       last_name: this.last_name,
  //       patronymic: this.patronymic,
  //       birthday: this.birthday.toISOString().substr(0, 10),
  //       phone_pacient: this.pacient_phone,
  //       // phone_doctor: "1312312312",
  //     };

  //     const res = await this.$store.dispatch(USER_REQUEST, data);
  //     this.loading = false;

  //     if (res) {
  //       this.applyBtn = false;
  //     } else {
  //       console.log("wrong");
  //     }
  //   },
  // },
};
</script>

<style>
.white-content.v-btn {
  color: white;
}
</style>
