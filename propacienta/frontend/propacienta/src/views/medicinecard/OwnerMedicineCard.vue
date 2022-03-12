<template>
  <div>
    <v-toolbar color="cyan" dark flat>
      <v-toolbar-title>Медицинская карта</v-toolbar-title>
    </v-toolbar>
    <v-tabs background-color="cyan" dark show-arrows centered>
      <v-tabs-slider color="yellow"></v-tabs-slider>
      <v-tab>Общие данные</v-tab>
      <v-tab>Исследования</v-tab>
      <v-tab>Анализы</v-tab>
      <v-tab>Хронические заболевания</v-tab>
      <v-tab-item>
        <OwnerMedicineCommonData :pacientId="pacientId">
        </OwnerMedicineCommonData>
      </v-tab-item>
      <v-tab-item>
        <OwnerMedicineCommonData :pacientId="pacientId">
        </OwnerMedicineCommonData>
      </v-tab-item>
      <v-tab-item>
        <OwnerMedicineCommonData :pacientId="pacientId">
        </OwnerMedicineCommonData>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
// import TextFieldUserOwner from "@/components/users/TextFieldUserOwner";
import OwnerMedicineCommonData from "@/components/medicinecard/CommonData";
import { INIT_PACIENT_STATE } from "@/store/actions/pacient";
// import DateFieldUserOwner from "@/components/users/DateFieldUserOwner";
// import { USER_REQUEST } from "@/store/actions/user";
export default {
  name: "OwnerMedicineCardView",
  props: {
    source: String,
  },
  components: {
    OwnerMedicineCommonData,
    // DateFieldUserOwner,
  },
  data: function () {
    return {
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
