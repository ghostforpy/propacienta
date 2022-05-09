<template>
  <div>
    <v-toolbar color="cyan" dark flat>
      <v-toolbar-title>Моя медицинская карта</v-toolbar-title>
    </v-toolbar>
    <v-tabs background-color="cyan" dark show-arrows centered v-model="page">
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
        <OwnerMedicineCardCommonData :pacientId="pacientId">
        </OwnerMedicineCardCommonData>
      </v-tab-item>
      <v-tab-item id="research">
        <OwnerMedicineIndependentResearch :pacientId="pacientId">
        </OwnerMedicineIndependentResearch>
      </v-tab-item>
      <v-tab-item id="analisis">
        <OwnerAnalisys :pacientId="pacientId"> </OwnerAnalisys>
      </v-tab-item>
      <v-tab-item id="transfered-diseases">
        <OwnerTransferedDiseases :pacientId="pacientId">
        </OwnerTransferedDiseases>
      </v-tab-item>
      <v-tab-item id="chronic-diseases">
        <OwnerChronicDiseases :pacientId="pacientId"> </OwnerChronicDiseases>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
// import TextFieldUserOwner from "@/components/users/TextFieldUserOwner";
import OwnerMedicineCardCommonData from "@/components/medicinecard/CommonData";
import OwnerMedicineIndependentResearch from "@/components/medicinecard/IndependentResearch";
import OwnerAnalisys from "@/components/medicinecard/OwnerAnalisys";
import OwnerTransferedDiseases from "@/components/medicinecard/OwnerTransferedDiseases";
import OwnerChronicDiseases from "@/components/medicinecard/OwnerChronicDiseases";
import { INIT_PACIENT_STATE } from "@/store/actions/pacient";
// import DateFieldUserOwner from "@/components/users/DateFieldUserOwner";
// import { USER_REQUEST } from "@/store/actions/user";
export default {
  name: "OwnerMedicineCardView",
  props: {
    source: String,
  },
  components: {
    OwnerMedicineCardCommonData,
    OwnerMedicineIndependentResearch,
    OwnerAnalisys,
    OwnerTransferedDiseases,
    OwnerChronicDiseases,
  },
  data: function () {
    return {
      page: "",
      // verticalTabs: false,
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
    await this.$store.dispatch(INIT_PACIENT_STATE, {
      pacient: this.$store.getters.pacient_id,
      medicine_card: this.$store.getters.medicine_card_id,
    });
    if (this.$route.hash != "") {
      this.page = this.$route.hash.replace("#", "");
    }
  },
  computed: {
    pacientId: function () {
      return this.$store.getters.pacient_id;
    },
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
        this.$router.replace({ name: this.$route.name, hash: hash });
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
