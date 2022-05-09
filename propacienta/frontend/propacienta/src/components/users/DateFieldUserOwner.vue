<template>
  <v-dialog
    ref="dialog"
    v-model="modal"
    :return-value.sync="date"
    persistent
    width="290px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        color="cyan"
        v-model="date"
        :label="labelname"
        prepend-icon="mdi-calendar"
        readonly
        v-bind="attrs"
        v-on="on"
        append-icon="mdi-pencil"
        @click:append="modal = true"
        ref="field"
        :rules="rules"
      ></v-text-field>
    </template>
    <v-date-picker
      v-model="date"
      color="cyan lighten-2"
      scrollable
      :max="maxDate"
    >
      <v-spacer></v-spacer>
      <v-btn text color="cyan" @click="modal = false"> Cancel </v-btn>
      <v-btn text color="cyan" @click="onOk"> OK </v-btn>
    </v-date-picker>
  </v-dialog>
</template>
<script>
export default {
  name: "DateFieldUserOwner",
  props: {
    fieldname: String,
    labelname: String,
    value: Date,
    rules: Array || undefined,
  },
  watch: {
    value: function (val) {
      if (this.val != "" && this.val != null) {
        this.date = val.toISOString().substr(0, 10);
      } else {
        this.date = "";
      }
    },
  },
  data: function () {
    return {
      date: "",
      modal: false,
      maxDate: new Date().toISOString().substr(0, 10),
    };
  },
  created: function () {
    if (this.value != "" && this.value != null) {
      this.date = this.value.toISOString().substr(0, 10);
    }
  },
  methods: {
    onOk: function () {
      this.$refs.dialog.save(this.date);
      this.$emit("input", new Date(this.date));
      this.$emit("updated", {
        fieldname: this.fieldname,
        content: this.content,
      });
    },
  },
};
</script>
