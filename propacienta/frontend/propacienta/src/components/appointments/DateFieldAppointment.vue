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
        prepend-inner-icon="mdi-calendar"
        readonly
        v-bind="attrs"
        v-on="on"
        append-icon="mdi-pencil"
        @click:append="modal = true"
        ref="field"
        :rules="rules"
        @click:prepend="handleClickPrepend"
        @click:append-outer="handleClickAppendOuter"
        :prepend-icon="leftDateAvail ? 'mdi-chevron-double-left' : ''"
        :append-outer-icon="rightDateAvail ? 'mdi-chevron-double-right' : ''"
      ></v-text-field>
    </template>
    <v-date-picker
      v-model="date"
      color="cyan lighten-2"
      scrollable
      :min="minDate"
      :allowed-dates="setAllowedDates"
      locale="ru-RU"
    >
      <v-spacer></v-spacer>
      <v-btn text color="cyan" @click="modal = false"> Отмена </v-btn>
      <v-btn text color="cyan" @click="onOk"> OK </v-btn>
    </v-date-picker>
  </v-dialog>
</template>
<script>
export default {
  name: "DateFieldAppointment",
  props: {
    fieldname: String,
    labelname: String,
    value: Date,
    rules: Array || undefined,
    allowedDates: Array || undefined,
  },
  watch: {
    value: function (val) {
      if (val != "" && val != null) {
        this.date = val.toISOString().substr(0, 10);
      } else {
        this.date = "";
      }
    },
  },
  data: function () {
    return {
      dateIdx: null,
      date: new Date().toISOString().substr(0, 10),
      modal: false,
      minDate: new Date().toISOString().substr(0, 10),
    };
  },
  created: function () {
    if (this.value != "" && this.value != null) {
      this.date = this.value.toISOString().substr(0, 10);
    }
  },
  computed: {
    rightDateAvail: function () {
      if (this.allowedDates.length <= 0) {
        return false;
      }
      var dIdx = this.getDateIdx();
      if (dIdx == null) {
        return true;
      }
      if (dIdx < this.allowedDates.length - 1) {
        return true;
      } else {
        return false;
      }
    },
    leftDateAvail: function () {
      if (this.allowedDates.length <= 0) {
        return false;
      }
      var dIdx = this.getDateIdx();
      if (dIdx == null) {
        return true;
      }
      if (dIdx > 0) {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
    getDateIdx: function () {
      var result = null;
      var el = this;
      this.allowedDates.forEach((item, idx) => {
        if (item === el.value.toISOString().substr(0, 10)) {
          result = idx;
          el.dateIdx = idx;
          return;
        }
      });
      return result;
    },
    setAllowedDates: function (val) {
      var result = false;
      this.allowedDates.forEach((item) => {
        if (item === val) {
          result = true;
        }
      });
      return result;
    },
    handleClickPrepend: function () {
      if (this.getDateIdx() == null) {
        this.setDate(this.allowedDates[0]);
      } else {
        this.setDate(this.allowedDates[this.dateIdx - 1]);
      }
    },

    handleClickAppendOuter: function () {
      if (this.getDateIdx() == null) {
        this.setDate(this.allowedDates[0]);
      } else {
        this.setDate(this.allowedDates[this.dateIdx + 1]);
      }
    },
    setDate: function (date) {
      this.date = date;
      this.onOk();
    },
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
