<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md8>
        <v-row class="cursor-auto">
          <AppointmentOrder
            v-model="dialog"
            :doctorId="doctorId"
            :pacientId="$store.getters.pacient_id"
          >
          </AppointmentOrder>
          <v-col cols="6" offset="3" offset-md="0" md="4" lg="3" class=""
            ><v-img contain class="rounded img" :src="avatarSrc">
              <v-tooltip
                bottom
                class="align-self-start"
                v-if="$store.getters.isAuthenticated"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    large
                    color="yellow lighten-1"
                    @click="toogleIsTreatingDoctorStar"
                    v-bind="attrs"
                    v-on="on"
                  >
                    {{ isTreatingDoctorStar }}
                  </v-icon>
                </template>
                <span>{{ treatingDoctorTooltip }}</span>
              </v-tooltip>
            </v-img>
            <v-btn
              small
              class="mt-2 white-content"
              style="width: 100%"
              color="cyan lighten-2"
              rounded
              @click="reserveHanlder"
            >
              Записаться на приём
            </v-btn>
            <v-tooltip
              bottom
              class="align-self-start"
              v-if="$store.getters.isAuthenticated"
              :disabled="isTreatingDoctor"
            >
              <template v-slot:activator="{ on }">
                <div v-on="on">
                  <v-btn
                    small
                    class="mt-2 white-content"
                    style="width: 100%"
                    color="cyan lighten-2"
                    rounded
                    @click="messageHandler"
                    :disabled="!isTreatingDoctor"
                  >
                    Написать сообщение
                  </v-btn>
                </div>
              </template>
              <span>Написать сообщение можно только своему лечащему врачу</span>
            </v-tooltip>
          </v-col>
          <v-col cols="12" md="7">
            <v-text-field
              fieldname="firstName"
              label="Фамилия"
              :value="firstName"
              ref="firstName"
              readonly
            >
            </v-text-field>
            <v-text-field
              fieldname="lastName"
              label="Имя"
              :value="lastName"
              ref="lastName"
              readonly
            >
            </v-text-field>
            <v-text-field
              fieldname="patronymic"
              label="Отчество"
              :value="patronymic"
              ref="patronymic"
              readonly
            >
            </v-text-field>

            <v-select
              v-model="fullSpec"
              :items="specializations.concat(...subSpecializations)"
              chips
              label="Специализации"
              multiple
              readonly
              class="spec"
            >
              <!-- <template #item="{ item }">
                {{ item.title }}
              </template> -->
              <template #selection="{ item }">
                <v-chip small>{{ item.title }}</v-chip>
              </template>
            </v-select>
            <v-textarea
              v-if="portfolio != null && portfolio != ''"
              rows="1"
              auto-grow
              label="Портфолио"
              fieldname="portfolio"
              :value="portfolio"
              ref="portfolio"
              readonly
            >
            </v-textarea>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import request_service from "@/api/HTTP";
import AppointmentOrder from "@/components/appointments/AppointmentOrder";
export default {
  name: "DoctorProfile",
  components: {
    AppointmentOrder,
  },
  data: function () {
    return {
      // doctorId: "",
      firstName: "",
      dialog: false,
      avatarSrc: require("@/assets/default_doctor_avatar.png"),
      lastName: "",
      patronymic: "",
      phone: "",
      portfolio: "",
      specializations: [],
      subSpecializations: [],

      isTreatingDoctor: false,
    };
  },
  computed: {
    doctorId: function () {
      return parseInt(this.$route.params.doctorId);
    },
    isTreatingDoctorStar: function () {
      return this.isTreatingDoctor ? "mdi-star" : "mdi-star-outline";
    },
    treatingDoctorTooltip: function () {
      return this.isTreatingDoctor
        ? "Является Вашим лечащим врачём"
        : "Сделать Вашим лечащим врачём";
    },
    fullSpec: function () {
      return this.specializations.concat(...this.subSpecializations);
    },
  },
  methods: {
    reserveHanlder: function () {
      this.dialog = true;
    },
    messageHandler: function () {
      console.log("handle msg");
    },
    toogleIsTreatingDoctorStar: function () {
      // добавить метод добавления в лечащие врачи
      let config = {
        method: "post",
        url: `api/doctors/${this.doctorId}/treating_doctor/`,
      };
      var el = this;
      request_service(
        config,
        function () {
          el.isTreatingDoctor = !el.isTreatingDoctor;
        }
        // function (error) {
        //   console.log(error);
        //   console.log(error.response);
        // }
      );
      // this.isTreatingDoctor = !this.isTreatingDoctor;
    },
  },
  mounted: async function () {
    if (this.doctorId == this.$store.getters.doctor_id) {
      this.$router.push({ name: "my-doctor-profile" });
      return;
    }
    let config = {
      method: "get",
      url: `api/doctors/${this.doctorId}/`,
    };
    var el = this;
    request_service(
      config,
      function (resp) {
        // console.log(resp);
        el.firstName = resp.data.first_name;
        el.lastName = resp.data.last_name;
        el.patronymic = resp.data.patronymic;
        el.phone = resp.data.phone;
        el.avatarSrc =
          resp.data.avatar != null ? resp.data.avatar : el.avatarSrc;
        el.portfolio = resp.data.portfolio;
        el.specializations = resp.data.specializations;
        el.subSpecializations = resp.data.sub_specializations;
        el.isTreatingDoctor = resp.data.treating_doctor;
      },
      function (error) {
        // console.log(error);
        // console.log(error.response);
        if (error.response.status == 404) {
          // console.log(404);
          el.$router.push({ name: "notfound" });
          return;
        }
        el.$router.push({ name: "main" });
        return;
      }
    );
  },
};
</script>

<style>
.img > .v-responsive__content {
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
}
.spec i {
  display: none !important;
}
.white-content.v-btn {
  color: white;
}
</style>
