<template>
  <v-card>
    <v-card-text class="d-flex justify-space-between">
      <div>{{ result }}</div>
      <div>{{ computedStamp }}</div>
    </v-card-text>
    <v-card-actions class="d-flex justify-end">
      <v-btn text color="red lighten-2" @click="$emit('delete', id)">
        Удалить
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
export default {
  name: "IndependentResearchResultCard",
  props: {
    id: Number,
    result: String,
    stamp: String,
  },
  // components: {
  //   TextFieldUserOwner,
  // },
  data: function () {
    return {};
  },
  computed: {
    computedStamp: function () {
      let d = new Date(this.stamp);
      return d.toLocaleString();
    },
  },

  // mounted: async function () {
  //   let config = {
  //     method: "get",
  //     url: "api/independent-researchs/",
  //   };
  //   var el = this;
  //   request_service(
  //     config,
  //     function (resp) {
  //       el.items.push(...resp.data);
  //     },
  //     function (error) {
  //       console.log(error.response);
  //     }
  //   );
  // },
  // methods: {
  //   handleChangeSelect: function () {
  //     let config = {
  //       params: {
  //         researchId: this.select.id,
  //       },
  //       method: "get",
  //       url: "api/independent-research-results/my/",
  //     };
  //     request_service(
  //       config,
  //       function (resp) {
  //         console.log(resp);
  //       },
  //       function (error) {
  //         console.log(error.response);
  //       }
  //     );
  //   },
  // },
};
</script>
