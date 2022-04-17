<template>
  <v-card>
    <div class="d-flex justify-space-between align-center">
      <v-card-title class="text-h8 py-1"> {{ lastName }} </v-card-title>
      <v-card-title class="py-1 text-body-2"
        >Дата рождения: {{ birthday }}</v-card-title
      >
    </div>
    <v-card-subtitle class="py-1"
      >{{ firstName }} {{ patronymic }}</v-card-subtitle
    >
  </v-card>
</template>
<script>
export default {
  name: "PacientListCard",
  props: {
    // id: Number,
    firstName: String,
    lastName: String,
    patronymic: String,
    birthday: String,
  },
  data: function () {
    return {};
  },
  computed: {},
  methods: {},
};
</script>
<style>
.break-word {
  word-break: break-word;
}

/* .birthday {
  margin-top: 0px !important;
} */
</style>