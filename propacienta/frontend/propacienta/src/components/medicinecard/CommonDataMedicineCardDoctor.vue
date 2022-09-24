<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md8>
        <v-row>
          <AppointmentOrder
            v-model="dialog"
            :doctorId="$store.getters.doctor_id"
            :pacientId="pacientId"
            :docMode="true"
          >
          </AppointmentOrder>
          <v-col cols="12" md="4"
            ><v-skeleton-loader
              class="mx-auto"
              max-width="200"
              type="image"
            ></v-skeleton-loader>
            <v-btn
              small
              class="mt-2 white-content"
              style="width: 100%"
              color="cyan lighten-2"
              rounded
              @click="reserveHanlder"
            >
              Записать на приём
            </v-btn>

            <v-btn
              small
              class="mt-2 white-content"
              style="width: 100%"
              color="cyan lighten-2"
              rounded
              @click="messageHandler"
            >
              Написать сообщение
            </v-btn>

            <v-btn
              small
              class="mt-2 white-content"
              style="width: 100%"
              color="cyan lighten-2"
              rounded
              @click="dialHandler"
              :disabled="!$store.getters.dialsOnline"
              :loading="dialBtn"
            >
              Позвонить
            </v-btn>
          </v-col>
          <v-col cols="12" md="6">
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
            <v-text-field
              fieldname="birthday"
              label="Дата рождения"
              :value="birthday"
              ref="birthday"
              readonly
            >
            </v-text-field>
            <v-text-field
              fieldname="phone"
              label="Телефон"
              :value="phone"
              ref="phone"
              readonly
            >
            </v-text-field>
            <TextFieldUserOwner
              fieldname="height"
              labelname="Рост"
              v-model="height"
              @updated="updateHandl"
              :rules="numberRules"
              ref="height"
              suffix="см"
            >
            </TextFieldUserOwner>
            <TextFieldUserOwner
              fieldname="weight"
              labelname="Вес"
              v-model="weight"
              @updated="updateHandl"
              :rules="numberRules"
              ref="weight"
              suffix="кг"
            >
            </TextFieldUserOwner>

            <v-btn
              block
              v-if="applyBtn"
              color="cyan"
              class="white-content"
              :loading="loading"
              :disabled="!(submitAvailable && !loading)"
              @click="onSubmit"
            >
              <span v-if="!loading"
                ><v-icon left> mdi-check </v-icon> Применить
              </span>
              <v-progress-circular
                v-else
                indeterminate
                color="primary"
              ></v-progress-circular>
            </v-btn>
          </v-col>
          <v-snackbar color="red lighten-1" centered v-model="snackbar">
            Что-то пошло не так.
            <template v-slot:action="{ attrs }">
              <v-btn text v-bind="attrs" @click="snackbar = false"> Ок </v-btn>
            </template>
          </v-snackbar>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import TextFieldUserOwner from "@/components/users/TextFieldUserOwner";
import request_service from "@/api/HTTP";
import AppointmentOrder from "@/components/appointments/AppointmentOrder";
export default {
  name: "CommonDataMedicineCardDoctor",
  props: {
    pacientId: Number,
    medicineCard: Number,
    firstName: String,
    lastName: String,
    patronymic: String,
    birthday: String,
    phone: String,
  },
  components: {
    TextFieldUserOwner,
    AppointmentOrder,
  },
  data: function () {
    return {
      height: "",
      oldHeight: "",
      weight: "",
      oldWeight: "",
      applyBtn: false,
      loading: false,
      dialog: false,
      snackbar: false,
      dialBtn: false,
      numberRules: [
        (value) => !!value || "Это поле является обязательным.",
        (value) => {
          const pattern = /^[1-2]?\d\d([.,]\d\d?)?$/g;
          return pattern.test(value) || "Неправильный формат.";
        },
      ],
    };
  },
  watch: {
    medicineCard: function () {
      let config = {
        method: "get",
        url: `api/medicine-cards/${this.medicineCard}/`,
        headers: {
          IsDoctor: true,
        },
      };
      var el = this;
      request_service(
        config,
        function (resp) {
          el.height = resp.data.height;
          el.weight = resp.data.weight;
        },
        function (error) {
          console.log(error.response);
        }
      );
    },
    // weight: function (val, oldVal) {
    //   console.log(val, oldVal);
    // },
  },
  computed: {
    submitAvailable: function () {
      const v =
        this.height != null &&
        this.height != "" &&
        this.weight != null &&
        this.weight != "" &&
        this.$refs.height.$refs.field.valid &&
        this.$refs.weight.$refs.field.valid;
      return v;
    },
  },
  mounted: function () {
    var el = this;
    this.$eventBus.$on("errorOpenPacientChat", () => {
      el.snackbar = true;
    });
    this.$eventBus.$on("initDialEnd", () => {
      el.dialBtn = false;
    });
  },
  methods: {
    dialHandler: function () {
      this.dialBtn = true;
      var that = this;
      this.$eventBus.$emit("initDial", {
        opponentId: this.pacientId,
        opponentType: "pacient",
      });
      setInterval(() => {
        that.dialBtn = false;
      }, 5000);
    },
    messageHandler: function () {
      this.$eventBus.$emit("openPacientChat", this.pacientId);
    },
    updateHandl: function () {
      if (this.height != this.oldHeight) {
        this.applyBtn = true;
      }
      if (this.weight != this.oldweight) {
        this.applyBtn = true;
      }
    },
    reserveHanlder: function () {
      this.dialog = true;
    },
    onSubmit: async function () {
      this.loading = true;
      let data = {
        height: this.height,
        weight: this.weight,
      };
      let config = {
        method: "patch",
        url: `api/medicine-cards/${this.medicineCard}/`,
        data: data,
        headers: {
          IsDoctor: true,
        },
      };
      var el = this;
      request_service(
        config,
        function (resp) {
          // console.log(resp);
          el.applyBtn = false;
          el.oldHeight = resp.data.height;
          el.oldWeight = resp.data.weight;
          el.loading = false;
        },
        function (error) {
          console.log(error.response);
        }
      );
    },
  },
};
</script>
<style>
.white-content.v-btn {
  color: white;
}
</style>