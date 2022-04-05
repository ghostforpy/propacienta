<template>
  <v-expansion-panel>
    <v-expansion-panel-header>{{ computedDisease }}</v-expansion-panel-header>
    <v-expansion-panel-content class="break-word"
      >Диагноз: {{ cDiagnosis }}<br />Дата постановки диагноза:
      {{ computed_stamp_diagnosis_date }}<br />Дата начала лечения:
      {{ computed_stamp_treatment_date }}<br />Дата окончания лечения:
      {{ computed_stamp_treatment_end_date }}
      <v-card-actions class="d-flex justify-end pm-0">
        <v-btn text color="red lighten-2" @click="$emit('delete', id)">
          Удалить
        </v-btn>
      </v-card-actions>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>
<script>
// import request_service from "@/api/HTTP";
export default {
  name: "TransferedDiseasesCard",
  props: {
    id: Number,
    disease: String,
    diagnosis: String,
    stamp_diagnosis_date: String,
    stamp_treatment_date: String,
    stamp_treatment_end_date: String,
  },
  data: function () {
    return {};
  },
  computed: {
    cDiagnosis: function () {
      return this.diagnosis;
    },
    computedDisease: function () {
      return this.disease;
    },
    computed_stamp_diagnosis_date: function () {
      let d = new Date(this.stamp_diagnosis_date);
      return d.toLocaleDateString();
    },
    computed_stamp_treatment_date: function () {
      let d = new Date(this.stamp_treatment_date);
      return d.toLocaleDateString();
    },
    computed_stamp_treatment_end_date: function () {
      let d = new Date(this.stamp_treatment_end_date);
      return d.toLocaleDateString();
    },
  },
  methods: {
    // deleteFileImg: function (id, url, event, type) {
    //   event.preventDefault();
    //   var el = this;
    //   console.log(url);
    //   let config = {
    //     method: "delete",
    //     url: url,
    //   };
    //   request_service(
    //     config,
    //     function () {
    //       console.log("sucess");
    //       if (type == "files") {
    //         el.fils = el.fils.filter((item, idx) => {
    //           return idx != id;
    //         });
    //       } else {
    //         el.imgs = el.imgs.filter((item, idx) => {
    //           return idx != id;
    //         });
    //       }
    //     },
    //     function (error) {
    //       console.log(error);
    //     }
    //   );
    // },
  },
};
</script>
<style>
.break-word {
  word-break: break-word;
}
</style>