<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md8>
        <v-row>
          <v-col cols="12">
            <v-select
              v-model="select"
              :items="items"
              label="Исследования"
              item-text="title"
              item-value="id"
              return-object
              @change="handleChangeSelect"
            ></v-select
          ></v-col>
          <v-col cols="12">
            <!-- компонент для добавления -->
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
// import {
//   MEDICINECARD_COMMON_GET,
//   MEDICINECARD_COMMON_PATCH_REQUEST,
// } from "@/store/actions/pacient";
import request_service from "@/api/HTTP";
export default {
  name: "OwnerMedicineIndependentResearch",
  props: {
    pacientId: Number,
  },
  components: {
    IndependentResearchResultCard,
  },
  data: function () {
    return {
      select: {},
      cache: new Map(),
      cacheNextPage: new Map(),
      items: [],
      results: [],
      loading: false,
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
    deleteHanlder: function (event) {
      var el = this;
      let config = {
        method: "delete",
        url: `api/independent-research-results/${this.pacientId}/${this.select.id}/${event}/`,
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
        url: `api/independent-research-results/${this.pacientId}/${this.select.id}/`,
        params: {
          page: this.cacheNextPage.get(this.select.id),
        },
      };
      request_service(
        config,
        function (resp) {
          console.log(resp);
          if (el.cache.has(el.select.id)) {
            el.results = el.cache.get(el.select.id);
            el.results.push(...resp.data.results);
          } else {
            el.cache.set(el.select.id, resp.data.results);
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