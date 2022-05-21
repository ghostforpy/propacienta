<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md6>
        <v-row>
          <!-- начало формы диалога -->
          <v-dialog v-model="dialog" max-width="600px">
            <v-card>
              <v-card-title>
                <span class="text-h5">Добавить выписной эпикриз</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <DateFieldUserOwner
                        fieldname="epicrisDateAdd"
                        labelname="Дата"
                        v-model="epicrisDateAdd"
                      ></DateFieldUserOwner>
                    </v-col>
                    <v-col cols="12">
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
                        :rules="notEmptyRules"
                      ></v-textarea>
                    </v-col>
                    <v-col cols="12">
                      <v-file-input
                        show-size
                        counter
                        multiple
                        label="Файлы"
                        ref="filesAdd"
                        @change="changeFiles"
                        accept=".pdf|.doc|.docx"
                        :rules="notEmptyRules"
                      ></v-file-input>
                    </v-col>
                    <v-col cols="12">
                      <v-file-input
                        show-size
                        counter
                        multiple
                        label="Изображения"
                        ref="imagesAdd"
                        @change="changeImages"
                        prepend-icon="mdi-file-image"
                        accept=".png|.jpg|.jpeg"
                        :rules="notEmptyRules"
                      ></v-file-input>
                    </v-col>
                    <small style="color: #ff5252" v-if="error"
                      >*Хотя бы одно из полей должно быть заполнено.</small
                    >
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
          <v-col cols="12">
            <v-autocomplete
              v-model="select"
              :items="items"
              label="Заболевания"
              item-text="title"
              :filter="filterAutocomplete"
              item-value="id"
              return-object
              @change="handleChangeSelect"
              :loading="loading"
            >
              <template #item="{ item }">
                <span>{{ item.title }} (код {{ item.code }})</span>
                <v-icon v-if="item.diseases_count > 0" color="pink"
                  >mdi-circle-medium</v-icon
                >
              </template>
              <template #selection="{ item }">
                <span>{{ item.title }} (код {{ item.code }})</span>
              </template>
            </v-autocomplete>
            <div class="d-flex justify-center" v-if="select != null">
              <v-btn
                class="ma-1 mb-2 white-content"
                color="cyan lighten-3"
                rounded
                @click="dialog = !dialog"
              >
                Добавить
              </v-btn>
            </div>
            <v-card v-if="results.length > 0" class="box-shadow-card-none">
              <v-expansion-panels inset multiple>
                <DischargeEpicrisCard
                  v-for="item in results"
                  :key="item.id"
                  v-on:delete="deleteHanlder"
                  :id="item.id"
                  :epicris="item.epicris"
                  :stamp="item.d"
                  :images="item.discharge_epicrisis_images"
                  :files="item.discharge_epicrisis_files"
                />
              </v-expansion-panels>
              <div class="d-flex justify-center">
                <v-btn
                  v-if="cacheNextPage.get(select.id) != null"
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
              <v-card-text v-if="select != null">
                <div class="text--primary">
                  Выписных эпикризов по выбранному хроническому заболеванию пока
                  нет.
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
import DischargeEpicrisCard from "./DischargeEpicrisCard";
// import TextFieldUserOwner from "../users/TextFieldUserOwner";
import DateFieldUserOwner from "../users/DateFieldUserOwner";
// import TimeFieldUserOwner from "../users/TimeFieldUserOwner";
// import {
//   MEDICINECARD_COMMON_GET,
//   MEDICINECARD_COMMON_PATCH_REQUEST,
// } from "@/store/actions/pacient";
import request_service from "@/api/HTTP";
export default {
  name: "OwnerChronicDiseases",
  props: {
    pacientId: Number,
  },
  components: {
    DateFieldUserOwner,
    // TextFieldUserOwner,
    // TimeFieldUserOwner,
    DischargeEpicrisCard,
  },
  data: function () {
    return {
      select: null,
      cache: new Map(),
      cacheNextPage: new Map(),
      nextPage: 1,
      items: [],
      results: [],
      loading: false,
      dialog: false,
      epicrisDateAdd: new Date(),
      epicrisAdd: null,
      error: false,
      readonlyEpicrisTextArea: true,
      filesAdd: [],
      imagesAdd: [],
      notEmptyRules: [(value) => !!value || "Это поле является обязательным."],
    };
  },
  mounted: async function () {
    let config = {
      method: "get",
      url: "api/diseases/",
      params: {
        pacientId: this.pacientId,
        diseaseType: "chronic",
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
        resp.data.map((item) => {
          el.cacheNextPage.set(item.id, 1);
        });
      },
      function (error) {
        console.log(error.response);
      }
    );
    // this.getResults();
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
      this.epicrisAdd = "";
      this.epicrisDateAdd = new Date();
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
      if (itemA.d > itemB.d) {
        return 1;
      }
      if (itemA.d == itemB.d) {
        return 0;
      }
      if (itemA.d < itemB.d) {
        return -1;
      }
    },
    validateFields: function () {
      this.error = false;
      if (
        this.epicrisAdd == null &&
        (this.filesAdd.length == 0 || this.filesAdd == null) &&
        (this.imagesAdd.length == 0 || this.imagesAdd == null)
      ) {
        this.$refs.epicrisAdd.hasFocused = true;
        this.$refs.filesAdd.hasFocused = true;
        this.$refs.imagesAdd.hasFocused = true;
        this.error = true;
        return false;
      }
      // this.error = false;
      return true;
    },
    handleAdd: function () {
      if (!this.validateFields()) {
        return;
      }
      let form = new FormData();
      form.append("disease", this.select.id);
      form.append("pacient", this.pacientId);
      form.append("epicris", this.epicrisAdd);
      form.append(
        "d",
        `${this.epicrisDateAdd.getFullYear()}-${
          this.epicrisDateAdd.getMonth() + 1
        }-${this.epicrisDateAdd.getDate()}`
      );
      this.filesAdd.forEach((file) => {
        form.append("files", file);
      });
      this.imagesAdd.forEach((img) => {
        form.append("images", img);
      });
      let config = {
        method: "post",
        url: `api/chronic-diseases-epicrisis/${this.pacientId}/${this.select.id}/`,
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
          var res = el.cache.get(el.select.id);
          res.push(resp.data);
          res.sort(el.compareResults);
          el.cache.set(el.select.id, res);
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
        url: `api/chronic-diseases-epicrisis-delete/${this.pacientId}/${event}/`,
      };
      if (
        this.$store.getters.docMode &&
        this.$store.getters.pacient_id != this.pacientId
      ) {
        config.headers = { IsDoctor: true };
        // config.data.medicine_card = this.medicineCard;
      }
      request_service(
        config,
        function () {
          var res = el.cache.get(el.select.id);
          el.cache.set(
            el.select.id,
            res.filter(function (item) {
              return item.id != event;
            })
          );
          el.results = el.cache.get(el.select.id);
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
      if (this.cacheNextPage.get(this.select.id) == null) {
        return;
      }
      var el = this;
      let config = {
        method: "get",
        url: `api/chronic-diseases-epicrisis/${this.pacientId}/${this.select.id}/`,
        params: {
          page: this.cacheNextPage.get(this.select.id),
        },
      };
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
          if (el.cache.has(el.select.id)) {
            el.results = el.cache.get(el.select.id);
            let r = resp.data.results;
            r.sort(el.compareResults);
            el.results.push(...r);
          } else {
            let r = resp.data.results;
            r.sort(el.compareResults);
            el.cache.set(el.select.id, r);
            el.results = resp.data.results;
          }

          if (resp.data.next != null) {
            let nextUrl = new URL(resp.data.next);
            el.cacheNextPage.set(
              el.select.id,
              nextUrl.searchParams.get("page")
            );
          } else {
            el.cacheNextPage.set(el.select.id, null);
          }
        },
        function (error) {
          console.log(error.response);
        }
      );
    },
    handleChangeSelect: function () {
      this.selected = true;
      if (this.cache.has(this.select.id)) {
        this.results = this.cache.get(this.select.id);
      } else {
        this.getResults();
      }
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