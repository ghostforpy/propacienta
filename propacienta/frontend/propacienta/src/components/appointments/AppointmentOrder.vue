<template>
  <v-dialog v-model="dialog" persistent :max-width="maxWidth">
    <v-card>
      <v-card-title>
        <span class="text-h5">Запись на приём</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col>
              <DateFieldAppointment
                fieldname="appointmentDateAdd"
                labelname="Дата"
                v-model="appointmentDateAdd"
                :allowedDates="allowedDates"
                :rules="notEmptyRules"
                ref="appointmentDateAdd"
              ></DateFieldAppointment>
            </v-col>
          </v-row>
          <v-row>
            <template v-if="freeTimeSlots.length > 0">
              <v-col
                cols="4"
                md="3"
                v-for="item in freeTimeSlots"
                :key="item.timeslot"
              >
                <v-btn
                  class="white-content"
                  rounded
                  :outlined="item.timeslot != appointmentTimeAdd"
                  color="cyan"
                  @click="handleTime(item.timeslot)"
                >
                  {{ item.timeslot.slice(0, -3) }}
                </v-btn>
              </v-col>
            </template>
            <span v-else> На выбранную дату нет свободного времени. </span>
            <v-overlay :value="overlay" absolute>
              <v-progress-circular
                indeterminate
                size="64"
              ></v-progress-circular>
            </v-overlay>
          </v-row>
        </v-container>
      </v-card-text>
      <v-alert dense text type="error" v-if="errorAlert">
        {{ errorAlertText }}
      </v-alert>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="cyan darken-1" text @click="$emit('input', false)">
          Закрыть
        </v-btn>
        <v-btn
          color="cyan darken-1"
          text
          @click="handleAdd"
          :disabled="appointmentTimeAdd == null"
        >
          Записать<template v-if="!docMode">ся</template>
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-snackbar color="cyan" centered v-model="snackbar">
      Запись успешно добавлена
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar = false"> Ок </v-btn>
      </template>
    </v-snackbar>
  </v-dialog>
</template>
<script>
import DateFieldAppointment from "./DateFieldAppointment";
// import {
//   MEDICINECARD_COMMON_GET,
//   MEDICINECARD_COMMON_PATCH_REQUEST,
// } from "@/store/actions/pacient";
import request_service from "@/api/HTTP";
export default {
  name: "AppointmentOrder",
  props: {
    doctorId: Number,
    pacientId: Number,
    value: Boolean,
    docMode: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    DateFieldAppointment,
  },
  data: function () {
    return {
      allowedDates: [],
      errorAlert: false,
      errorAlertText: "Что-то пошло не так.",
      changed: false,
      dialog: this.value,
      snackbar: false,
      oldDocId: 0,
      overlay: false,
      appointmentDateAdd: new Date(),
      appointmentTimeAdd: null,
      freeTimeSlots: [],
      // maxWidth: this.$vuetify.breakpoint.smAndDown ? "600px" : "1000px",
      maxWidth: "600px",
      notEmptyRules: [(value) => !!value || "Это поле является обязательным."],
    };
  },
  watch: {
    value: function (val) {
      this.dialog = val;
      if (val && this.oldDocId != this.doctorId) {
        // this.appointmentDateAdd = new Date();
        this.getAllowedDates();
        this.getFreeTimeslost();
        this.appointmentTimeAdd = null;
        this.oldDocId = this.doctorId;
      }
    },
    appointmentDateAdd: function () {
      this.appointmentTimeAdd = null;
      this.getFreeTimeslost();
    },
  },

  methods: {
    getFreeTimeslost: function () {
      this.overlay = true;
      let config = {
        method: "get",
        url: "api/freetimeslots/",
        params: {
          doctor: this.doctorId,
          date: `${this.appointmentDateAdd.getFullYear()}-${
            this.appointmentDateAdd.getMonth() + 1
          }-${this.appointmentDateAdd.getDate()}`,
        },
      };
      var el = this;
      request_service(
        config,
        function (resp) {
          // console.log(resp);
          el.freeTimeSlots = [];
          resp.data.forEach((item) => {
            item.time_slots.forEach((slot) => {
              el.freeTimeSlots.push(slot);
            });
          });
        },
        function (error) {
          console.log(error.response);
        }
      );
      setTimeout(() => {
        this.overlay = false;
      }, 500);
    },
    getAllowedDates: function () {
      this.overlay = true;
      let config = {
        method: "get",
        url: "api/workdays/",
        params: {
          doctor: this.doctorId,
        },
      };
      var el = this;
      request_service(
        config,
        function (resp) {
          // console.log(resp);
          el.allowedDates = [];
          resp.data.forEach((item) => {
            el.allowedDates.push(item.date);
          });
          el.allowedDates.sort();
        },
        function (error) {
          console.log(error.response);
        }
      );
      setTimeout(() => {
        this.overlay = false;
      }, 500);
    },
    handleTime: function (timeslot) {
      this.appointmentTimeAdd = timeslot;
      this.appointmentDateAdd.setHours(
        parseInt(timeslot.slice(0, 2)),
        parseInt(timeslot.slice(3, 5))
      );
    },
    handleAdd: function () {
      this.overlay = true;
      let form = new FormData();
      form.append("doctor", this.doctorId);
      form.append("pacient", this.pacientId);
      form.append("dt", this.appointmentDateAdd.toISOString());

      let config = {
        method: "post",
        url: `api/pacient-appointments/`,
        data: form,
      };
      if (
        this.$store.getters.docMode &&
        this.$store.getters.pacientId != this.pacientId
      ) {
        config.headers = { IsDoctor: true };
        config.url = `api/doctor-appointments/`;
      }
      var el = this;
      request_service(
        config,
        function () {
          el.errorAlert = false;
          // console.log(resp);
          el.freeTimeSlots = el.freeTimeSlots.filter((item) => {
            return item.timeslot != el.appointmentTimeAdd;
          });
          el.snackbar = true;
          el.appointmentTimeAdd = null;
        },
        function (error) {
          el.errorAlert = true;
          el.errorAlertText = "Что-то пошло не так.";
          if (error.response.status === 400) {
            if (error.response.data.non_field_errors == "Timeslot is busy.") {
              el.errorAlertText = "Выбранное время уже кто-то занял.";
              el.freeTimeSlots = el.freeTimeSlots.filter((item) => {
                return item.timeslot != el.appointmentTimeAdd;
              });
              el.appointmentTimeAdd = null;
            }
          }
          // console.log(error);
        }
      );
      setTimeout(() => {
        this.overlay = false;
      }, 500);
    },
  },
};
</script>
<style>
.white-content.v-btn {
  color: white;
}
.box-shadow-card-none {
  box-shadow: none !important;
}
</style>