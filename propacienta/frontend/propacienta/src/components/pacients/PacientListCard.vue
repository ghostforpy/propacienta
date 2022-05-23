<template>
  <v-card class="pb-10">
    <div class="d-flex justify-space-between align-center">
      <v-card-title class="text-h8 py-1"> {{ lastName }} </v-card-title>
      <v-card-title class="py-1 text-body-2 d-md-flex d-none"
        >Дата рождения: {{ birthday }}</v-card-title
      >
    </div>
    <v-card-subtitle class="py-1"
      >{{ firstName }} {{ patronymic }}</v-card-subtitle
    >
    <v-card-title class="py-1 text-body-2 d-flex d-md-none"
      >Дата рождения: {{ birthday }}</v-card-title
    >
    <v-card-actions class="btn-position">
      <v-btn color="cyan darken-1" text @click="reserve($event)"
        >Записать на приём</v-btn
      >
    </v-card-actions>
  </v-card>
</template>
<script>
export default {
  name: "PacientListCard",
  props: {
    id: Number,
    firstName: String,
    lastName: String,
    patronymic: String,
    birthday: String,
  },
  data: function () {
    return {};
  },
  computed: {},
  methods: {
    reserve(event) {
      event.stopPropagation();
      event.preventDefault();
      this.$emit("reserve", this.id);
      // this.loading = true
      // setTimeout(() => (this.loading = false), 2000)
    },
  },
};
</script>
<style>
.break-word {
  word-break: break-word;
}
.btn-position.v-card__actions {
  position: absolute;
  right: 0px;
  bottom: 0px;
}

/* .birthday {
  margin-top: 0px !important;
} */
</style>