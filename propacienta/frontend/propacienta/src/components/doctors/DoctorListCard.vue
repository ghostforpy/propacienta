<template>
  <v-card height="100%" class="pb-10">
    <v-img contain max-height="220" :src="avatarSrc"></v-img>
    <v-card-title class="text-body-1">{{ lastName }}</v-card-title>
    <v-card-subtitle class="text-body-2"
      >{{ firstName }} {{ patronymic }}</v-card-subtitle
    >
    <v-card-subtitle class="text-body-2">
      <v-chip
        v-for="(item, id) in []
          .concat(specializations, subSpecializations)
          .slice(0, 3)"
        :key="id"
        class="mr-1 text-caption"
        x-small
      >
        {{ item.title }}
      </v-chip>
    </v-card-subtitle>
    <v-card-actions class="btn-position" v-if="id != $store.getters.doctor_id">
      <v-btn color="cyan darken-1" text @click="reserve($event)"
        >Записаться</v-btn
      >
    </v-card-actions>
  </v-card>
</template>
<script>
export default {
  name: "DoctorListCard",
  props: {
    id: Number,
    firstName: String,
    avatar: String,
    lastName: String,
    patronymic: String,
    specializations: Array,
    subSpecializations: Array,
  },
  data: function () {
    return {};
  },
  computed: {
    avatarSrc: function () {
      return this.avatar != null
        ? this.avatar
        : require("@/assets/default_doctor_avatar.png");
    },
  },
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
.doctor-avatar {
  border-top-left-radius: inherit;
  border-top-right-radius: unset !important;
  border-bottom-left-radius: inherit;
}
</style>