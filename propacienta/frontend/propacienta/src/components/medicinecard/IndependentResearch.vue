<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm5 md4>
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              v-model="select"
              :items="items"
              label="Исследования"
              item-text="title"
              item-value="id"
              return-object
              @change="handleChangeSelect"
            ></v-autocomplete
          ></v-col>
          <v-col cols="12">
            <v-card class="mb-2">
              <v-card-text>
                <TextFieldUserOwner
                  fieldname="result"
                  labelname="Результат"
                  v-model="resultAdd"
                  :rules="numberRules"
                  ref="result"
                >
                </TextFieldUserOwner>
                <DateFieldUserOwner
                  fieldname="resultDateAdd"
                  labelname="Дата"
                  v-model="resultDateAdd"
                ></DateFieldUserOwner>
                <TimeFieldUserOwner
                  fieldname="resultTimeAdd"
                  labelname="Время"
                  v-model="resultTimeAdd"
                ></TimeFieldUserOwner>
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
            <div v-if="results.length > 0">
              <div v-for="item in results" :key="item.id" class="mb-2">
                <IndependentResearchResultCard
                  v-on:delete="deleteHanlder"
                  :id="item.id"
                  :result="item.result"
                  :stamp="item.datetime_stamp"
                />
              </div>
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
            </div>
            <v-card v-else>
              <v-card-text>
                <div class="text--primary">Исследований пока не было.</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import IndependentResearchResultCard from "./IndependentResearchResultCard";
import TextFieldUserOwner from "../users/TextFieldUserOwner";
import DateFieldUserOwner from "../users/DateFieldUserOwner";
import TimeFieldUserOwner from "../users/TimeFieldUserOwner";
// import {
//   MEDICINECARD_COMMON_GET,
//   MEDICINECARD_COMMON_PATCH_REQUEST,
// } from "@/store/actions/pacient";
import request_service from "@/api/HTTP";
export default {
  name: "OwnerMedicineIndependentResearch",
  props: {
    pacientId: Number,
    medicineCard: Number,
  },
  components: {
    IndependentResearchResultCard,
    DateFieldUserOwner,
    TextFieldUserOwner,
    TimeFieldUserOwner,
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
      resultTimeAdd: "",
      selected: false,
      numberRules: [
        (value) => !!value || "Это поле является обязательным.",
        (value) => {
          const pattern = /^\d+$/g;
          return pattern.test(value) || "Неправильный формат.";
        },
      ],
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
      url: "api/independent-researchs/",
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
      if (/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/i.test(this.resultTimeAdd)) {
        this.resultDateAdd.setHours(
          this.resultTimeAdd.split(":")[0],
          this.resultTimeAdd.split(":")[1],
          0
        );
      }
      let config = {
        method: "post",
        url: `api/independent-research-results/${this.pacientId}/${this.select.id}/`,
        data: {
          independent_research: this.select.id,
          result: this.resultAdd,
          datetime_stamp: this.resultDateAdd,
          medicine_card: this.$store.getters.medicineCardId,
        },
      };
      if (
        this.$store.getters.docMode &&
        this.$store.getters.pacientId != this.pacientId
      ) {
        config.headers = { IsDoctor: true };
        config.data.medicine_card = this.medicineCard;
      }
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
        url: `api/independent-research-results/${this.pacientId}/${this.select.id}/${event}/`,
      };
      if (this.$store.getters.docMode) {
        config.headers = { IsDoctor: true };
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
        url: `api/independent-research-results/${this.pacientId}/${this.select.id}/`,
        params: {
          page: this.cacheNextPage.get(this.select.id),
        },
      };
      if (this.$store.getters.docMode) {
        config.headers = { IsDoctor: true };
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
</style>