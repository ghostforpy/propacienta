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
  data: function () {
    return {};
  },
  computed: {
    computedStamp: function () {
      let d = new Date(this.stamp);
      return d.toLocaleString();
    },
  },
};
</script>
