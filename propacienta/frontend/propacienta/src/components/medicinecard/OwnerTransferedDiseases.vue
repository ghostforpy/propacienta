<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md6>
        <v-row>
          <!-- начало формы диалога -->
          <v-col cols="12"
            ><v-autocomplete
              v-model="selectMain"
              :items="items"
              label="Заболевания"
              item-text="title"
              :filter="filterAutocomplete"
              item-value="id"
              return-object
              @change="handleChangeSelect"
            >
              <template #item="{ item }">
                <span>{{ item.title }} (код {{ item.code }})</span>
                <v-icon v-if="item.diseases_count > 0" color="pink"
                  >mdi-circle-medium</v-icon
                >
              </template>
              <template #selection="{ item }">
                <span>{{ item.title }} (код {{ item.code }})</span>
              </template></v-autocomplete
            ></v-col
          >
          <v-dialog v-model="dialog" :max-width="maxWidth">
            <v-card>
              <v-card-title>
                <span class="text-h5">Добавить перенесённое заболевание</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12"
                      ><v-autocomplete
                        v-model="selectDialog"
                        :items="items"
                        label="Заболевания"
                        item-text="title"
                        :filter="filterAutocomplete"
                        item-value="id"
                        return-object
                      >
                        <template #item="{ item }">
                          <span>{{ item.title }} (код {{ item.code }})</span>
                          <v-icon v-if="item.diseases_count > 0" color="pink"
                            >mdi-circle-medium</v-icon
                          >
                        </template>
                        <template #selection="{ item }">
                          <span>{{ item.title }} (код {{ item.code }})</span>
                        </template></v-autocomplete
                      ></v-col
                    >
                    <!-- ddadasd -->
                    <v-col cols="12" md="6">
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
                      <!-- </v-col>
                    <v-col cols="12"> -->
                      <DateFieldUserOwner
                        fieldname="diagnoseDateAdd"
                        labelname="Дата постановки диагноза"
                        v-model="diagnoseDateAdd"
                        :rules="notEmptyRules"
                        ref="diagnoseDateAdd"
                      ></DateFieldUserOwner>
                      <!-- </v-col>
                    <v-col cols="12"> -->
                      <DateFieldUserOwner
                        fieldname="startTreatmentDateAdd"
                        labelname="Дата начала лечения"
                        v-model="startTreatmentDateAdd"
                        :rules="notEmptyRules"
                        ref="startTreatmentDateAdd"
                      ></DateFieldUserOwner>
                      <!-- </v-col>
                    <v-col cols="12"> -->
                      <DateFieldUserOwner
                        fieldname="endTreatmentDateAdd"
                        labelname="Дата окончания лечения"
                        v-model="endTreatmentDateAdd"
                        :rules="notEmptyRules"
                        ref="endTreatmentDateAdd"
                      ></DateFieldUserOwner>
                    </v-col>
                    <!-- dasdad -->
                    <v-col cols="12" md="6">
                      <!-- </v-col>
                    <v-col cols="12"> -->
                      <v-textarea
                        v-model="epicrisAdd"
                        auto-grow
                        clearable
                        outlined
                        :readonly="readonlyEpicrisTextArea"
                        @change="changeTextArea"
                        @click:append="
                          readonlyEpicrisTextArea = !readonlyEpicrisTextArea
                        "
                        :append-icon="
                          readonlyEpicrisTextArea ? 'mdi-pencil' : 'mdi-check'
                        "
                        clear-icon="mdi-close-circle"
                        label="Эпикриз"
                        ref="epicrisAdd"
                      ></v-textarea>
                      <DateFieldUserOwner
                        fieldname="epicrisDateAdd"
                        labelname="Дата выписного эпикриза"
                        v-model="epicrisDateAdd"
                      ></DateFieldUserOwner>
                      <!-- </v-col>
                    <v-col cols="12"> -->
                      <v-file-input
                        show-size
                        counter
                        multiple
                        label="Файлы"
                        ref="filesAdd"
                        @change="changeFiles"
                        accept=".pdf|.doc|.docx"
                      ></v-file-input>
                      <!-- </v-col>
                    <v-col cols="12"> -->
                      <v-file-input
                        show-size
                        counter
                        multiple
                        label="Изображения"
                        ref="imagesAdd"
                        @change="changeImages"
                        prepend-icon="mdi-file-image"
                        accept=".png|.jpg|.jpeg"
                      ></v-file-input>
                    </v-col>
                    <!-- <small style="color: #ff5252" v-if="error"
                      >*Хотя бы одно из полей должно быть заполнено.</small
                    > -->
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="dialog = false">
                  Закрыть
                </v-btn>
                <v-btn color="blue darken-1" text @click="handleAdd">
                  Сохранить
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <!-- конец формы диалога -->
          <!-- <div class="d-flex justify-content-center"> -->
          <v-col cols="12" class="d-flex justify-center">
            <v-btn
              class="ma-1 mb-2 white-content"
              color="cyan lighten-3"
              rounded
              @click="dialog = !dialog"
            >
              Добавить
            </v-btn>
            <!-- </div> -->
          </v-col>
          <v-col cols="12">
            <!-- <v-card class="mb-2">
              <v-card-text> </v-card-text>
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
            </v-card> -->
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
                  :discharge_epicris="item.discharge_epicris"
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
    medicineCard: Number,
  },
  components: {
    DateFieldUserOwner,
    // TextFieldUserOwner,
    // TimeFieldUserOwner,
    TransferedDiseasesCard,
  },
  data: function () {
    return {
      selectMain: null,
      oldSelected: null,
      selectDialog: null,
      maxWidth: this.$vuetify.breakpoint.smAndDown ? "600px" : "1000px",
      // cache: new Map(),
      // cacheNextPage: new Map(),
      nextPage: 1,
      items: [],
      results: [],
      loading: false,
      dialog: false,
      diagnoseAdd: "",
      diagnoseDateAdd: null,
      epicrisDateAdd: null,
      epicrisAdd: null,
      error: false,
      readonlyDiarnoseTextArea: true,
      startTreatmentDateAdd: null,
      endTreatmentDateAdd: null,
      readonlyEpicrisTextArea: true,
      filesAdd: [],
      imagesAdd: [],
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
        diseaseType: "transferred",
      },
    };
    if (
      this.$store.getters.docMode &&
      this.$store.getters.pacient_id != this.pacientId
    ) {
      config.headers = { IsDoctor: true };
      // config.data.medicine_card = this.medicineCard;
    }
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
    filterAutocomplete: function (item, queryText) {
      return (
        item.title.toLocaleLowerCase().indexOf(queryText.toLocaleLowerCase()) >
          -1 ||
        item.code.toLocaleLowerCase().indexOf(queryText.toLocaleLowerCase()) >
          -1
      );
    },
    clearForm: function () {
      this.diagnoseAdd = "";
      this.epicrisDateAdd = null;
      this.startTreatmentDateAdd = null;
      this.endTreatmentDateAdd = null;
      this.epicrisAdd = "";
      this.epicrisDateAdd = new Date();
      // this.resultDateAdd = new Date();
      this.resultTimeAdd = "";
      this.filesAdd = [];
      this.imagesAdd = [];
    },
    changeFiles: function (event) {
      this.error = false;
      this.filesAdd = event;
    },
    changeImages: function (event) {
      this.error = false;
      this.imagesAdd = event;
    },
    changeTextArea: function () {
      this.error = false;
    },
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
      form.append("disease", this.selectDialog.id);
      form.append("pacient", this.pacientId);
      this.filesAdd.forEach((file) => {
        form.append("files", file);
      });
      this.imagesAdd.forEach((img) => {
        form.append("images", img);
      });
      if (
        this.$store.getters.docMode &&
        this.$store.getters.pacient_id != this.pacientId
      ) {
        form.append("medicine_card", this.medicineCard);
      } else {
        form.append("medicine_card", this.$store.getters.medicineCardId);
      }
      form.append("diagnosis", this.diagnoseAdd);
      form.append(
        "diagnosis_date",
        `${this.diagnoseDateAdd.getFullYear()}-${
          this.diagnoseDateAdd.getMonth() + 1
        }-${this.diagnoseDateAdd.getDate()}`
      );
      form.append("diagnosis_year", `${this.diagnoseDateAdd.getFullYear()}`);
      form.append(
        "treatment_date",
        `${this.startTreatmentDateAdd.getFullYear()}-${
          this.startTreatmentDateAdd.getMonth() + 1
        }-${this.startTreatmentDateAdd.getDate()}`
      );
      form.append(
        "treatment_end_date",
        `${this.endTreatmentDateAdd.getFullYear()}-${
          this.endTreatmentDateAdd.getMonth() + 1
        }-${this.endTreatmentDateAdd.getDate()}`
      );
      if (this.epicrisDateAdd != null) {
        form.append(
          "epicris_date",
          `${this.epicrisDateAdd.getFullYear()}-${
            this.epicrisDateAdd.getMonth() + 1
          }-${this.epicrisDateAdd.getDate()}`
        );
      }
      if (this.epicrisAdd != null) {
        form.append("epicris", this.epicrisAdd);
      }
      // console.log(form);
      let config = {
        method: "post",
        url: `api/transferred-diseases/${this.pacientId}/`,
        data: form,
      };
      if (
        this.$store.getters.docMode &&
        this.$store.getters.pacient_id != this.pacientId
      ) {
        config.headers = { IsDoctor: true };
        // config.data.medicine_card = this.medicineCard;
      }
      var el = this;
      request_service(
        config,
        function (resp) {
          if (el.selectMain == null) {
            el.results.push(resp.data);
            el.results.sort(el.compareResults);
          } else if (el.selectDialog.id == el.selectMain.id) {
            el.results.push(resp.data);
            el.results.sort(el.compareResults);
          }

          el.clearForm();
          el.dialog = false;
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
      if (
        this.$store.getters.docMode &&
        this.$store.getters.pacient_id != this.pacientId
      ) {
        config.headers = { IsDoctor: true };
      }
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
      if (this.nextPage == null && this.oldSelected == this.selectMain) {
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
      if (this.selectMain != null) {
        config.params.disease = this.selectMain.id;
        config.params.page = this.nextPage;
      }
      if (
        this.$store.getters.docMode &&
        this.$store.getters.pacient_id != this.pacientId
      ) {
        config.headers = { IsDoctor: true };
        // config.data.medicine_card = this.medicineCard;
      }
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
      this.nextPage = 1;
      this.results = [];
      this.selectDialog = this.selectMain;
      this.getResults();
      this.oldSelected = this.selectMain;
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