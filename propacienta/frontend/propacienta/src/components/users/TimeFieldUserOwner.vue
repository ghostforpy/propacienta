<template>
  <v-dialog
    ref="dialog"
    v-model="modal"
    :return-value.sync="time"
    persistent
    width="290px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="time"
        readonly
        v-bind="attrs"
        v-on="on"
        color="cyan"
        :label="labelname"
        prepend-icon="mdi-clock-time-four-outline"
        append-icon="mdi-pencil"
        @click:append="modal = true"
        ref="field"
      ></v-text-field>
    </template>
    <v-time-picker
      v-if="modal"
      v-model="time"
      full-width
      format="24hr"
      color="cyan"
    >
      <v-spacer></v-spacer>
      <v-btn text color="cyan lighten-2" @click="modal = false"> Cancel </v-btn>
      <v-btn text color="cyan lighten-2" @click="onOk"> OK </v-btn>
    </v-time-picker>
  </v-dialog>
</template>
<script>
export default {
  name: "TimeFieldUserOwner",
  props: {
    fieldname: String,
    labelname: String,
    value: String,
  },
  watch: {
    value: function (val) {
      this.time = val;
    },
  },
  data: function () {
    return {
      time: "",
      modal: false,
    };
  },
  // created: function () {
  //   if (this.value != "") {
  //     this.date = this.value.toISOString().substr(0, 10);
  //   }
  // },
  methods: {
    onOk: function () {
      this.$refs.dialog.save(this.time);
      this.$emit("input", this.time);
      // this.$emit("updated", {
      //   fieldname: this.fieldname,
      //   content: this.content,
      // });
    },
  },
};
</script>
