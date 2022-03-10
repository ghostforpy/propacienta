<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md8>
        <v-row>
          <v-col cols="12" md="3"
            ><v-skeleton-loader
              class="mx-auto"
              max-width="200"
              type="image"
            ></v-skeleton-loader
          ></v-col>
          <v-col cols="12" md="9">
            <!-- <v-form> -->
            <v-text-field
              name="email"
              label="Адрес электронной почты"
              type="text"
              v-model="email"
              readonly
            ></v-text-field>
            <TextFieldUserOwner
              fieldname="first_name"
              labelname="Имя"
              v-model="first_name"
              @updated="updateHandl"
              :rules="textRules"
            >
            </TextFieldUserOwner>
            <TextFieldUserOwner
              fieldname="last_name"
              labelname="Фамилия"
              v-model="last_name"
              @updated="updateHandl"
              :rules="textRules"
            >
            </TextFieldUserOwner>
            <TextFieldUserOwner
              fieldname="patronymic"
              labelname="Отчество"
              v-model="patronymic"
              @updated="updateHandl"
              :rules="textRules"
            >
            </TextFieldUserOwner>
            <TextFieldUserOwner
              fieldname="pacient_phone"
              labelname="Телефон пациента"
              v-model="pacient_phone"
              @updated="updateHandl"
              :rules="phoneRules"
              ref="pacient_phone"
            >
            </TextFieldUserOwner>
            <DateFieldUserOwner
              fieldname="birthday"
              labelname="Дата рождения"
              v-model="birthday"
              @updated="updateHandl"
            >
            </DateFieldUserOwner>
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
            <!-- </v-form> -->
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import TextFieldUserOwner from "@/components/users/TextFieldUserOwner";
import DateFieldUserOwner from "@/components/users/DateFieldUserOwner";
import { USER_REQUEST } from "@/store/actions/user";
export default {
  name: "ProfileOwnerPacientView",
  props: {
    source: String,
  },
  components: {
    TextFieldUserOwner,
    DateFieldUserOwner,
  },
  data: function () {
    return {
      email: "",
      first_name: "",
      last_name: "",
      patronymic: "",
      pacient_phone: "",
      birthday: new Date(),
      applyBtn: false,
      loading: false,
      textRules: [(value) => !!value || "Это поле является обязательным."],
      phoneRules: [
        (value) => !!value || "Это поле является обязательным.",
        (value) => {
          const pattern = /^[+]*[0-9]{11}$/g;
          return pattern.test(value) || "Неправильный формат номера.";
        },
      ],
    };
  },
  mounted: function () {
    this.email = this.$store.state.user.email;
    this.first_name = this.$store.state.user.first_name;
    this.last_name = this.$store.state.user.last_name;
    this.patronymic = this.$store.state.user.patronymic;
    this.pacient_phone = this.$store.state.user.pacient_phone;
    if (this.$store.state.user.birthday != undefined) {
      this.birthday = new Date(this.$store.state.user.birthday);
    }
  },
  computed: {
    submitAvailable: function () {
      const v =
        this.first_name != null &&
        this.first_name != "" &&
        this.last_name != null &&
        this.last_name != "" &&
        this.patronymic != null &&
        this.patronymic != "" &&
        this.pacient_phone != null &&
        this.pacient_phone != "";
      return v;
    },
  },
  methods: {
    toggleFirstNameReadonly: function () {
      this.firstNameReadonly = !this.firstNameReadonly;
    },
    updateHandl: function () {
      if (
        this.first_name != this.$store.state.user.first_name ||
        this.last_name != this.$store.state.user.last_name ||
        this.patronymic != this.$store.state.user.patronymic ||
        this.pacient_phone != this.$store.state.user.pacient_phone ||
        this.birthday.toISOString().substr(0, 10) !=
          new Date(this.$store.state.user.birthday).toISOString().substr(0, 10)
      ) {
        this.applyBtn = true;
      } else {
        this.applyBtn = false;
      }
    },
    onSubmit: async function () {
      if (!this.$refs.pacient_phone.$refs.field.valid) {
        return;
      }
      this.loading = true;
      let data = {
        first_name: this.first_name,
        last_name: this.last_name,
        patronymic: this.patronymic,
        birthday: this.birthday.toISOString().substr(0, 10),
        phone_pacient: this.pacient_phone,
        // phone_doctor: "1312312312",
      };

      const res = await this.$store.dispatch(USER_REQUEST, data);
      this.loading = false;

      if (res) {
        this.applyBtn = false;
      } else {
        console.log("wrong");
      }
    },
  },
};
</script>

<style>
.white-content.v-btn {
  color: white;
}
</style>
