<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md6>
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              v-model="select"
              :items="items"
              label="Анализы"
              item-text="title"
              item-value="id"
              return-object
              @change="handleChangeSelect"
            >
              <template #item="{ item }">
                <span>{{ item.title }}</span>
                <v-chip
                  v-if="item.results_count > 0"
                  color="pink"
                  small
                  text-color="white"
                >
                  {{ item.results_count }}
                </v-chip>
              </template>
              <template #selection="{ item }">
                <span>{{ item.title }}</span>
                <v-chip
                  v-if="item.results_count > 0"
                  color="pink"
                  small
                  text-color="white"
                >
                  {{ item.results_count }}
                </v-chip>
              </template>
            </v-autocomplete></v-col
          >
          <v-col cols="12">
            <v-card class="mb-2">
              <v-card-text>
                <TextFieldUserOwner
                  fieldname="result"
                  labelname="Результат"
                  v-model="resultAdd"
                  ref="result"
                >
                </TextFieldUserOwner>
                <DateFieldUserOwner
                  fieldname="resultDateAdd"
                  labelname="Дата"
                  v-model="resultDateAdd"
                ></DateFieldUserOwner>
                <v-file-input
                  show-size
                  counter
                  multiple
                  label="Файлы"
                  ref="files"
                  @change="changeFiles"
                  accept=".pdf|.doc|.docx"
                ></v-file-input>
                <v-file-input
                  show-size
                  counter
                  multiple
                  label="Изображения"
                  ref="images"
                  @change="changeImages"
                  prepend-icon="mdi-file-image"
                  accept=".png|.jpg|.jpeg"
                ></v-file-input>
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
                <AnalisysResultCard
                  v-for="item in results"
                  :key="item.id"
                  v-on:delete="deleteHanlder"
                  :id="item.id"
                  :result="item.result"
                  :stamp="item.d"
                  :images="item.analysis_images"
                  :files="item.analysis_files"
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
              <v-card-text>
                <div class="text--primary">Анализов пока не было.</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import AnalisysResultCard from "./AnalisysResultCard";
import TextFieldUserOwner from "../users/TextFieldUserOwner";
import DateFieldUserOwner from "../users/DateFieldUserOwner";
// import TimeFieldUserOwner from "../users/TimeFieldUserOwner";
// import {
//   MEDICINECARD_COMMON_GET,
//   MEDICINECARD_COMMON_PATCH_REQUEST,
// } from "@/store/actions/pacient";
import request_service from "@/api/HTTP";
export default {
  name: "OwnerAnalisys",
  props: {
    pacientId: Number,
  },
  components: {
    DateFieldUserOwner,
    TextFieldUserOwner,
    // TimeFieldUserOwner,
    AnalisysResultCard,
  },
  data: function () {
    return {
      select: {},
      cache: new Map(),
      cacheNextPage: new Map(),
      items: [],
      results: [],
      loading: false,
      resultAdd: "",
      resultDateAdd: new Date(),
      // resultTimeAdd: "",
      filesAdd: [],
      imagesAdd: [],
      selected: false,
      numberRules: [(value) => !!value || "Это поле является обязательным."],
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
      url: "api/analisys/",
      params: {
        pacientId: this.pacientId,
      },
    };
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
  },
  methods: {
    clearForm: function () {
      this.resultAdd = "";
      // this.resultDateAdd = new Date();
      this.resultTimeAdd = "";
    },
    changeFiles: function (event) {
      this.filesAdd = event;
    },
    changeImages: function (event) {
      this.imagesAdd = event;
    },
    compareResults: function (itemA, itemB) {
      if (itemA.datetime_stamp > itemB.datetime_stamp) {
        return 1;
      }
      if (itemA.datetime_stamp == itemB.datetime_stamp) {
        return 0;
      }
      if (itemA.datetime_stamp < itemB.datetime_stamp) {
        return -1;
      }
    },
    handleAdd: function () {
      if (!this.$refs.result.$refs.field.valid) {
        return;
      }
      let form = new FormData();
      this.filesAdd.forEach((file) => {
        form.append("files", file);
      });
      this.imagesAdd.forEach((img) => {
        form.append("images", img);
      });
      form.append("analysis", this.select.id);
      form.append("pacient", this.pacientId);
      form.append("medicine_card", this.$store.getters.medicineCardId);
      form.append("result", this.resultAdd);
      form.append(
        "d",
        `${this.resultDateAdd.getFullYear()}-${
          this.resultDateAdd.getMonth() + 1
        }-${this.resultDateAdd.getDate()}`
      );
      // console.log(form);
      let config = {
        method: "post",
        url: `api/analysis-results/${this.pacientId}/${this.select.id}/`,
        data: form,
        headers: {
          Accept: "application/json",
          "Content-Type": "multipart/form-data",
        },
      };

      var el = this;
      request_service(
        config,
        function (resp) {
          var res = el.cache.get(el.select.id);
          res.push(resp.data);
          res.sort(el.compareResults);
          el.cache.set(el.select.id, res);
          el.results = el.cache.get(el.select.id);
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
        url: `api/analysis-results-delete/${this.pacientId}/${event}/`,
      };
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
        url: `api/analysis-results/${this.pacientId}/${this.select.id}/`,
        params: {
          page: this.cacheNextPage.get(this.select.id),
        },
      };
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