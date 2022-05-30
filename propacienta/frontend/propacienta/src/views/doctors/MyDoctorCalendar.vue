<template>
  <div>
    <v-toolbar color="cyan" dark flat>
      <v-toolbar-title>Мой календарь</v-toolbar-title>
    </v-toolbar>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs10 sm8 md8>
          <AppointmentOrder
            v-model="dialogOrder"
            :doctorId="$store.getters.doctor_id"
            :pacientId="selectedEvent.pacient"
            :docMode="true"
            v-on:order="handleOrderAdd"
          >
          </AppointmentOrder>
          <v-col>
            <v-sheet height="64">
              <v-toolbar flat>
                <v-btn
                  outlined
                  class="mr-4"
                  color="grey darken-2"
                  @click="setToday"
                >
                  Сегодня
                </v-btn>
                <v-btn fab text small color="grey darken-2" @click="prev">
                  <v-icon small> mdi-chevron-left </v-icon>
                </v-btn>
                <v-btn fab text small color="grey darken-2" @click="next">
                  <v-icon small> mdi-chevron-right </v-icon>
                </v-btn>
                <v-toolbar-title
                  v-if="$refs.calendar && $vuetify.breakpoint.mdAndUp"
                >
                  {{ $refs.calendar.title }}
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-menu bottom right>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      outlined
                      color="grey darken-2"
                      v-bind="attrs"
                      v-on="on"
                    >
                      <span>{{ typeToLabel[type] }}</span>
                      <v-icon right> mdi-menu-down </v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="type = 'day'">
                      <v-list-item-title>День</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="type = 'week'">
                      <v-list-item-title>Неделя</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="type = 'month'">
                      <v-list-item-title>Месяц</v-list-item-title>
                    </v-list-item>
                    <!-- <v-list-item @click="type = '4day'">
                      <v-list-item-title>4 days</v-list-item-title>
                    </v-list-item> -->
                  </v-list>
                </v-menu>
              </v-toolbar>
            </v-sheet>
            <v-sheet height="600">
              <v-snackbar
                color="cyan"
                centered
                :timeout="5000"
                v-model="cancel_appointment_snackbar"
              >
                Отменить запись на приём?
                <v-alert
                  dense
                  text
                  type="error"
                  v-if="errorСancelAppointmentAlert"
                >
                  Что-то пошло не так.
                </v-alert>
                <template v-slot:action="{ attrs }">
                  <v-btn text v-bind="attrs" @click="cancelAppointmentHandle">
                    Да
                  </v-btn>
                  <v-btn
                    text
                    v-bind="attrs"
                    @click="cancel_appointment_snackbar = false"
                  >
                    Нет
                  </v-btn>
                </template>
              </v-snackbar>
              <v-calendar
                ref="calendar"
                v-model="focus"
                color="cyan"
                locale="ru-RU"
                :events="events"
                :event-color="getEventColor"
                :type="type"
                first-time="06:00"
                @click:event="showEvent"
                @click:more="viewDay"
                @click:date="viewDay"
                @change="updateRange"
                event-more-text="Ещё {0} приёма"
                weekdays="1, 2, 3, 4, 5, 6, 0"
              ></v-calendar>
              <v-menu
                v-model="selectedOpen"
                :close-on-content-click="false"
                :activator="selectedElement"
                offset-x
              >
                <v-card color="grey lighten-4" min-width="350px" flat>
                  <v-toolbar :color="selectedEvent.color" dark>
                    <!-- <v-btn icon>
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn> -->
                    <v-toolbar-title
                      v-html="selectedEvent.name"
                    ></v-toolbar-title>
                    <v-spacer></v-spacer>
                    <!-- <v-btn icon>
                      <v-icon>mdi-heart</v-icon>
                    </v-btn> -->
                    <v-btn icon @click="selectedOpen = false">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-toolbar>
                  <v-card-text
                    v-if="selectedEvent != null && selectedEvent != undefined"
                  >
                    <!-- <span v-html="selectedEvent.details"></span> -->
                    <div v-if="selectedEvent.start != undefined">
                      Время приема: {{ showTime(selectedEvent.start) }} -
                      {{ showTime(selectedEvent.end) }}
                    </div>
                    <router-link
                      class="pacient-card-calendar"
                      :to="{
                        name: 'pacient-medicine-card',
                        params: { pacientId: selectedEvent.pacient },
                      }"
                      ><v-btn icon>
                        <v-icon>mdi-book-open-variant</v-icon></v-btn
                      >Медицинская карта</router-link
                    >
                  </v-card-text>
                  <v-card-actions>
                    <v-btn
                      text
                      color="secondary"
                      @click="cancel_appointment_snackbar = true"
                    >
                      Отменить приём
                    </v-btn>
                    <v-btn text color="secondary" @click="dialogOrder = true">
                      Записать на другое время
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-menu>
            </v-sheet>
          </v-col>
        </v-flex></v-layout
      ></v-container
    >
  </div>
</template>

<script>
import request_service from "@/api/HTTP";
import AppointmentOrder from "@/components/appointments/AppointmentOrder";

export default {
  name: "MyDoctorCalendar",
  components: { AppointmentOrder },
  data: () => ({
    dialogOrder: false,
    focus: "",
    type: "month",
    typeToLabel: {
      month: "Месяц",
      week: "Неделя",
      day: "День",
      // "4day": "4 Days",
    },
    // calendarView: true,
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    cancel_appointment_snackbar: false,
    errorСancelAppointmentAlert: false,
    events: [],
    colors: [
      "blue",
      "indigo",
      "deep-purple",
      "cyan",
      "green",
      "orange",
      "grey darken-1",
    ],
  }),
  mounted() {
    this.$refs.calendar.checkChange();
  },
  methods: {
    showTime: function (dt) {
      let hours = dt.getHours();
      if (hours < 10) {
        hours = `0${hours}`;
      }
      let minutes = dt.getMinutes();
      if (minutes < 10) {
        minutes = `0${minutes}`;
      }
      return `${hours}:${minutes}`;
    },
    viewDay({ date }) {
      this.focus = date;
      this.type = "day";
    },
    getEventColor(event) {
      return event.color;
    },
    setToday() {
      this.focus = "";
    },
    prev() {
      this.$refs.calendar.prev();
    },
    next() {
      this.$refs.calendar.next();
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event;
        this.selectedElement = nativeEvent.target;
        requestAnimationFrame(() =>
          requestAnimationFrame(() => (this.selectedOpen = true))
        );
      };

      if (this.selectedOpen) {
        this.selectedOpen = false;
        requestAnimationFrame(() => requestAnimationFrame(() => open()));
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    },
    updateRange({ start, end }) {
      this.events = [];
      let viewStart = this.$refs.calendar.getStartOfWeek(start);
      let viewEnd = this.$refs.calendar.getEndOfWeek(end);
      const min = new Date(`${viewStart.date}T00:00:00`);
      const max = new Date(`${viewEnd.date}T23:59:59`);
      this.getAppointments(min.toISOString(), max.toISOString());
    },
    handleOrderAdd: function (event, order) {
      if (event == true) {
        this.cancelAppointmentHandle();
        order.start = new Date(order.dt);
        order.end = new Date(order.end);
        order.color = this.colors[this.rnd(0, this.colors.length - 1)];
        order.timed = true;
        this.events.push(order);
      }
    },
    cancelAppointmentHandle: function () {
      var el = this;
      let config = {
        method: "delete",
        url: `api/doctor-appointments/${this.selectedEvent.id}/`,
      };
      this.errorСancelAppointmentAlert = false;
      request_service(
        config,
        function () {
          // console.log(resp.data);
          el.cancel_appointment_snackbar = false;
          el.events = el.events.filter((item) => {
            return item.id != el.selectedEvent.id;
          });
        },
        function (error) {
          el.errorСancelAppointmentAlert = true;
          console.log(error.response);
        }
      );
    },
    getAppointments: async function (start, end) {
      var el = this;
      let config = {
        method: "get",
        url: `api/doctor-appointments/`,
        params: {
          dt_after: start,
          dt_before: end,
          // calendar: this.calendarView,
        },
      };
      await request_service(
        config,
        function (resp) {
          // console.log(resp.data);
          resp.data.forEach((element) => {
            element.start = new Date(element.dt);
            element.end = new Date(element.end);
            element.color = el.colors[el.rnd(0, el.colors.length - 1)];
            element.timed = true;
            el.events.push(element);
          });
        },
        function (error) {
          console.log(error.response);
        }
      );
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a;
    },
  },
};
</script>

<style>
.img > .v-responsive__content {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  align-items: flex-end;
}
.pacient-card-calendar {
  all: unset;
  color: rgb(83, 83, 83) !important;
  text-decoration: none;
}
</style>
