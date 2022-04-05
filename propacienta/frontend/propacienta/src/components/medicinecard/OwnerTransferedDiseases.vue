<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md6>
        <v-row>
          <v-col cols="12">
            <v-card class="mb-2">
              <v-card-text>
                <v-select
                  v-model="select"
                  :items="items"
                  label="Заболевания"
                  item-text="title"
                  item-value="id"
                  return-object
                  @change="handleChangeSelect"
                ></v-select>
                <!-- <TextFieldUserOwner
                  fieldname="diagnose"
                  labelname="Диагноз"
                  v-model="diagnoseAdd"
                  ref="diagnose"
                >
                </TextFieldUserOwner> -->
                <v-textarea
                  v-model="diagnoseAdd"
                  auto-grow
                  clearable
                  outlined
                  :readonly="readonlyDiarnoseTextArea"
                  @click:append="
                    readonlyDiarnoseTextArea = !readonlyDiarnoseTextArea
                  "
                  :append-icon="
                    readonlyDiarnoseTextArea ? 'mdi-pencil' : 'mdi-check'
                  "
                  clear-icon="mdi-close-circle"
                  label="Диагноз"
                  ref="diagnose"
                  :rules="notEmptyRules"
                ></v-textarea>
                <DateFieldUserOwner
                  fieldname="diagnoseDateAdd"
                  labelname="Дата постановки диагноза"
                  v-model="diagnoseDateAdd"
                  :rules="notEmptyRules"
                  ref="diagnoseDateAdd"
                ></DateFieldUserOwner>
                <DateFieldUserOwner
                  fieldname="startTreatmentDateAdd"
                  labelname="Дата начала лечения"
                  v-model="startTreatmentDateAdd"
                  :rules="notEmptyRules"
                  ref="startTreatmentDateAdd"
                ></DateFieldUserOwner>
                <DateFieldUserOwner
                  fieldname="endTreatmentDateAdd"
                  labelname="Дата окончания лечения"
                  v-model="endTreatmentDateAdd"
                  :rules="notEmptyRules"
                  ref="endTreatmentDateAdd"
                ></DateFieldUserOwner>
              </v-card-text>
              <v-card-actions class="d-flex justify-end">
                <v-btn
                  text
                  color="cyan lighten-2"
                  @click="handleAdd"
                  :disabled="!selected"
                >
                  Добавить
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card v-if="results.length > 0" class="box-shadow-card-none">
              <v-expansion-panels inset multiple>
                <TransferedDiseasesCard
                  v-for="item in results"
                  :key="item.id"
                  v-on:delete="deleteHanlder"
                  :id="item.id"
                  :disease="item.disease_title"
                  :diagnosis="item.diagnosis"
                  :stamp_diagnosis_date="item.diagnosis_date"
                  :stamp_treatment_date="item.treatment_date"
                  :stamp_treatment_end_date="item.treatment_end_date"
                />
              </v-expansion-panels>
              <div class="d-flex justify-center">
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
              </div>
            </v-card>
            <v-card v-else>
              <v-card-text>
                <div class="text--primary">
                  Перенесённых заболеваний пока не было.
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import TransferedDiseasesCard from "./TransferedDiseasesCard";
// import TextFieldUserOwner from "../users/TextFieldUserOwner";
import DateFieldUserOwner from "../users/DateFieldUserOwner";
// import TimeFieldUserOwner from "../users/TimeFieldUserOwner";
// import {
//   MEDICINECARD_COMMON_GET,
//   MEDICINECARD_COMMON_PATCH_REQUEST,
// } from "@/store/actions/pacient";
import request_service from "@/api/HTTP";
export default {
  name: "OwnerTransferedDiseases",
  props: {
    pacientId: Number,
  },
  components: {
    DateFieldUserOwner,
    // TextFieldUserOwner,
    // TimeFieldUserOwner,
    TransferedDiseasesCard,
  },
  data: function () {
    return {
      select: {},
      // cache: new Map(),
      // cacheNextPage: new Map(),
      nextPage: 1,
      items: [],
      results: [],
      loading: false,
      diagnoseAdd: "",
      diagnoseDateAdd: null,
      readonlyDiarnoseTextArea: true,
      startTreatmentDateAdd: null,
      endTreatmentDateAdd: null,
      // resultTimeAdd: "",
      // filesAdd: [],
      // imagesAdd: [],
      selected: false,
      notEmptyRules: [(value) => !!value || "Это поле является обязательным."],
    };
  },
  // watch: {
  //   height: function (val, oldVal) {
  //     console.log(val, oldVal);
  //   },
  //   weight: function (val, oldVal) {
  //     console.log(val, oldVal);
  //   },
  // },
  // computed: {
  //   submitAvailable: function () {
  //     const v =
  //       this.height != null &&
  //       this.height != "" &&
  //       this.weight != null &&
  //       this.weight != "" &&
  //       this.$refs.height.$refs.field.valid &&
  //       this.$refs.weight.$refs.field.valid;
  //     return v;
  //   },
  // },
  mounted: async function () {
    let config = {
      method: "get",
      url: "api/diseases/",
      params: {
        pacientId: this.pacientId,
      },
    };
    var el = this;
    request_service(
      config,
      function (resp) {
        el.items.push(...resp.data);
        // resp.data.map((item) => {
        //   el.cacheNextPage.set(item.id, 1);
        // });
      },
      function (error) {
        console.log(error.response);
      }
    );
    this.getResults();
  },
  methods: {
    clearForm: function () {
      this.resultAdd = "";
      // this.resultDateAdd = new Date();
      this.resultTimeAdd = "";
    },
    // changeFiles: function (event) {
    //   this.filesAdd = event;
    // },
    // changeImages: function (event) {
    //   this.imagesAdd = event;
    // },
    compareResults: function (itemA, itemB) {
      if (itemA.stamp_diagnosis_date > itemB.stamp_diagnosis_date) {
        return 1;
      }
      if (itemA.stamp_diagnosis_date == itemB.stamp_diagnosis_date) {
        return 0;
      }
      if (itemA.stamp_diagnosis_date < itemB.stamp_diagnosis_date) {
        return -1;
      }
    },
    validateFields: function () {
      if (!this.$refs.diagnose.valid) {
        this.$refs.diagnose.hasFocused = true;
        return false;
      }
      if (!this.$refs.diagnoseDateAdd.$refs.field.valid) {
        this.$refs.diagnoseDateAdd.$refs.field.hasFocused = true;
        return false;
      }
      if (!this.$refs.startTreatmentDateAdd.$refs.field.valid) {
        this.$refs.startTreatmentDateAdd.$refs.field.hasFocused = true;
        return false;
      }
      if (!this.$refs.endTreatmentDateAdd.$refs.field.valid) {
        this.$refs.endTreatmentDateAdd.$refs.field.hasFocused = true;
        return false;
      }
      return true;
    },
    handleAdd: function () {
      if (!this.validateFields()) {
        return;
      }
      let form = new FormData();
      form.append("disease", this.select.id);
      form.append("pacient", this.pacientId);
      form.append("medicine_card", this.$store.getters.medicineCardId);
      form.append("diagnosis", this.diagnoseAdd);
      form.append(
        "diagnosis_date",
        `${this.diagnoseDateAdd.getFullYear()}-${this.diagnoseDateAdd.getMonth()}-${this.diagnoseDateAdd.getDate()}`
      );
      form.append("diagnosis_year", `${this.diagnoseDateAdd.getFullYear()}`);
      form.append(
        "treatment_date",
        `${this.startTreatmentDateAdd.getFullYear()}-${this.startTreatmentDateAdd.getMonth()}-${this.startTreatmentDateAdd.getDate()}`
      );
      form.append(
        "treatment_end_date",
        `${this.endTreatmentDateAdd.getFullYear()}-${this.endTreatmentDateAdd.getMonth()}-${this.endTreatmentDateAdd.getDate()}`
      );
      // console.log(form);
      let config = {
        method: "post",
        url: `api/transferred-diseases/${this.pacientId}/`,
        data: form,
      };

      var el = this;
      request_service(
        config,
        function (resp) {
          // var res = el.cache.get(el.select.id);
          // res.push(resp.data);
          // res.sort(el.compareResults);
          // el.cache.set(el.select.id, res);
          el.results.push(resp.data);
          el.clearForm();
        },
        function (error) {
          console.log(error);
        }
      );
    },
    deleteHanlder: function (event) {
      var el = this;
      let config = {
        method: "delete",
        url: `api/transferred-diseases-delete/${this.pacientId}/${event}/`,
      };
      request_service(
        config,
        function () {
          // var res = el.cache.get(el.select.id);
          // el.cache.set(
          //   el.select.id,
          //   res.filter(function (item) {
          //     return item.id != event;
          //   })
          // );
          el.results = el.results.filter(function (item) {
            return item.id != event;
          });
        },
        function (error) {
          console.log(error);
        }
      );
    },
    loadHandler: function () {
      this.loading = true;
      this.getResults();
      setTimeout(() => (this.loading = false), 500);
    },
    getResults: function () {
      if (this.nextPage == null) {
        return;
      }
      var el = this;
      let config = {
        method: "get",
        url: `api/transferred-diseases/${this.pacientId}/`,
        params: {
          page: this.nextPage,
        },
      };
      request_service(
        config,
        function (resp) {
          // console.log(resp);
          // if (el.cache.has(el.select.id)) {
          //   el.results = el.cache.get(el.select.id);
          let r = resp.data.results;
          r.sort(el.compareResults);
          el.results.push(...r);
          // } else {
          // let r = resp.data.results;
          // r.sort(el.compareResults);
          // // el.cache.set(el.select.id, r);
          // el.results = resp.data.results;
          // }

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
    handleChangeSelect: function () {
      this.selected = true;
      // if (this.cache.has(this.select.id)) {
      //   this.results = this.cache.get(this.select.id);
      // } else {
      //   this.getResults();
      // }
    },
  },
};
</script>
<style>
.white-content.v-btn {
  color: white;
}
.box-shadow-card-none {
  box-shadow: none !important;
}
</style>