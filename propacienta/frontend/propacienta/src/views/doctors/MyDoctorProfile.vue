<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs10 sm8 md8>
        <v-row class="cursor-auto">
          <v-col cols="6" offset="3" offset-md="0" md="4" lg="3" class=""
            ><v-img contain class="rounded img" :src="avatarSrc">
              <v-tooltip v-if="avatarChanged" right class="align-self-start">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    large
                    color="cyan lighten-1"
                    @click="cancelEditAvatar"
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-close-circle-outline
                  </v-icon>
                </template>
                <span>Отменить</span>
              </v-tooltip>
              <v-tooltip v-if="avatarChanged" right class="align-self-start">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    large
                    color="cyan lighten-1"
                    @click="submitAvatar"
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-check
                  </v-icon>
                </template>
                <span>Применить</span>
              </v-tooltip>
              <v-tooltip
                right
                v-if="
                  avatarSrc != require('@/assets/default_doctor_avatar.png') &&
                  !avatarChanged
                "
                class="align-self-start"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    large
                    color="cyan lighten-1"
                    @click="deleteAvatar"
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-cancel
                  </v-icon>
                </template>
                <span>Удалить</span>
              </v-tooltip>
              <v-tooltip right class="align-self-start">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    large
                    color="cyan lighten-1"
                    @click="editAvatar"
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-image-edit-outline
                  </v-icon>
                </template>
                <span>Изменить</span>
              </v-tooltip>
            </v-img>
            <v-file-input
              class="d-none"
              show-size
              counter
              ref="avatar"
              v-model="avatar"
              @change="previewAvatar"
              accept=".png|.jpg|.jpeg"
            ></v-file-input>
          </v-col>
          <v-col cols="12" md="7">
            <v-text-field
              color="cyan"
              label="Телефон"
              v-model="phone"
              :readonly="fieldPhoneReadonly"
              :clearable="!fieldPhoneReadonly"
              @click:append="fieldPhoneEditSubmit"
              :append-icon="fieldPhoneReadonly ? 'mdi-pencil' : 'mdi-check'"
              :rules="phoneRules"
              ref="phone"
            ></v-text-field>
            <v-autocomplete
              :append-outer-icon="fieldSpecializationsEdit ? 'mdi-check' : ''"
              @click:append-outer="fieldSpecializationsEditSubmit"
              @change="fieldSpecializationsEdit = true"
              v-model="mySpecializations"
              :items="specializations"
              dense
              color="cyan"
              item-color="cyan"
              chips
              label="Специализации"
              multiple
              item-text="title"
              return-object
            >
              <template #selection="{ item }">
                <v-chip
                  small
                  class="mb-1"
                  v-bind="item.attrs"
                  :input-value="item.selected"
                  close
                  @click:close="removeSpecialization(item)"
                >
                  {{ item.title }}
                </v-chip>
              </template>
            </v-autocomplete>
            <v-autocomplete
              :append-outer-icon="
                fieldSubSpecializationsEdit ? 'mdi-check' : ''
              "
              @click:append-outer="fieldSubSpecializationsEditSubmit"
              @change="fieldSubSpecializationsEdit = true"
              v-model="mySubSpecializations"
              :items="subSpecializations"
              dense
              color="cyan"
              item-color="cyan"
              chips
              label="Узкие специализации"
              multiple
              item-text="title"
              return-object
            >
              <template #selection="{ item }">
                <v-chip
                  small
                  class="mb-1"
                  v-bind="item.attrs"
                  :input-value="item.selected"
                  close
                  @click:close="removeSubSpecialization(item)"
                >
                  {{ item.title }}
                </v-chip>
              </template>
            </v-autocomplete>
            <v-textarea
              v-model="portfolio"
              auto-grow
              rows="1"
              color="cyan"
              clearable
              :readonly="readonlyPortfolioTextArea"
              @click:append="clickAppendTextArea"
              @click:clear="readonlyPortfolioTextArea = false"
              :append-icon="
                readonlyPortfolioTextArea ? 'mdi-pencil' : 'mdi-check'
              "
              clear-icon="mdi-close-circle"
              label="Портфолио"
              ref="portfolio"
            ></v-textarea>
          </v-col>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import request_service from "@/api/HTTP";
export default {
  name: "MyDoctorProfile",
  components: {},
  data: function () {
    return {
      avatarSrc: require("@/assets/default_doctor_avatar.png"),
      oldAvatarSrc: "",
      avatar: null,
      avatarChanged: false,
      phone: "",
      fieldPhoneReadonly: true,
      portfolio: "",
      oldPortfolio: "",
      mySpecializations: [],
      fieldSpecializationsEdit: false,
      mySubSpecializations: [],
      fieldSubSpecializationsEdit: false,
      specializations: [],
      subSpecializations: [],
      readonlyPortfolioTextArea: true,
      submitAvailable: false,
      phoneRules: [
        (value) => {
          const pattern = /^[+]*[0-9]{11}$/g;
          return pattern.test(value) || "Неправильный формат номера.";
        },
      ],
    };
  },
  computed: {
    doctorId: function () {
      return parseInt(this.$store.getters.doctor_id);
    },

    // fullSpec: function () {
    //   return this.specializations.concat(...this.subSpecializations);
    // },
  },
  methods: {
    patchDoctor: async function (doctor_data) {
      let config = {
        method: "patch",
        url: `api/doctors/${this.$store.getters.doctor_id}/`,
        data: doctor_data,
      };
      var el = this;
      request_service(
        config,
        function () {
          if (doctor_data.specializations != undefined) {
            el.fieldSpecializationsEdit = false;
          }
          if (doctor_data.sub_pecializations != undefined) {
            el.fieldSubSpecializationsEdit = false;
          }
          if (doctor_data.portfolio != undefined) {
            el.readonlyPortfolioTextArea = true;
          }
          if (doctor_data.phone != undefined) {
            el.fieldPhoneReadonly = true;
          }
          if (doctor_data instanceof FormData) {
            if (doctor_data.has("avatar")) {
              el.avatarChanged = false;
              el.avatar = null;
            }
          }
        },
        function (error) {
          console.log(error);
          console.log(error.response);
        }
      );
    },
    removeSpecialization: function (item) {
      this.fieldSpecializationsEdit = true;
      this.mySpecializations = this.mySpecializations.filter(function (it) {
        return it.id != item.id;
      });
    },
    removeSubSpecialization: function (item) {
      this.fieldSubSpecializationsEdit = true;
      this.mySubSpecializations = this.mySubSpecializations.filter(function (
        it
      ) {
        return it.id != item.id;
      });
    },
    fieldSpecializationsEditSubmit: function () {
      let data = {
        specializations: this.mySpecializations.map((item) => {
          return item.id;
        }),
      };
      this.patchDoctor(data);
    },
    fieldSubSpecializationsEditSubmit: function () {
      let data = {
        sub_specializations: this.mySubSpecializations.map((item) => {
          return item.id;
        }),
      };
      this.patchDoctor(data);
    },
    fieldPhoneEditSubmit: function () {
      if (this.fieldPhoneReadonly) {
        this.fieldPhoneReadonly = !this.fieldPhoneReadonly;
      } else {
        if (this.$refs.phone.valid) {
          let data = {
            phone: this.phone,
          };
          this.patchDoctor(data);
        }
      }
    },
    previewAvatar: function () {
      this.avatarChanged = true;
      this.oldAvatarSrc = this.avatarSrc;
      this.avatarSrc = URL.createObjectURL(this.avatar);
    },
    editAvatar: function () {
      this.$refs.avatar.$refs.input.click();
    },
    cancelEditAvatar: function () {
      this.avatarChanged = false;
      this.avatarSrc = this.oldAvatarSrc;
    },
    submitAvatar: function () {
      let form = new FormData();
      form.append("avatar", this.avatar);
      this.patchDoctor(form);
    },
    deleteAvatar: function () {
      let config = {
        method: "delete",
        url: `api/doctors/${this.$store.getters.doctor_id}/delete_avatar/`,
      };
      var el = this;
      request_service(
        config,
        function () {
          el.avatar = null;
          el.avatarSrc = require("@/assets/default_doctor_avatar.png");
          el.avatarChanged = false;
        },
        function (error) {
          console.log(error);
          console.log(error.response);
        }
      );
    },
    clickAppendTextArea: function () {
      if (this.readonlyPortfolioTextArea) {
        this.readonlyPortfolioTextArea = !this.readonlyPortfolioTextArea;
      } else {
        let data = {
          portfolio: this.portfolio,
        };
        this.patchDoctor(data);
      }
    },
  },
  mounted: async function () {
    let config = {
      method: "get",
      url: `api/doctors/${this.$store.getters.doctor_id}/`,
    };
    var el = this;
    request_service(
      config,
      function (resp) {
        // console.log(resp);
        // el.firstName = resp.data.first_name;
        // el.lastName = resp.data.last_name;
        // el.patronymic = resp.data.patronymic;
        el.phone = resp.data.phone;
        el.avatarSrc =
          resp.data.avatar != null ? resp.data.avatar : el.avatarSrc;
        el.portfolio = resp.data.portfolio;
        el.oldPortfolio = resp.data.portfolio;
        el.mySpecializations = resp.data.specializations;
        el.mySubSpecializations = resp.data.sub_specializations;
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
    config = {
      method: "get",
      url: `api/doctors-specializations/`,
    };
    request_service(
      config,
      function (resp) {
        // console.log(resp.data);
        resp.data.forEach((item) => {
          el.specializations.push({ id: item.id, title: item.title });
          item.sub_specializations.forEach((item) => {
            el.subSpecializations.push({ id: item.id, title: item.title });
          });
        });
      },
      function (error) {
        console.log(error);
        // console.log(error.response);
        // if (error.response.status == 404) {
        //   // console.log(404);
        //   el.$router.push({ name: "notfound" });
        //   return;
        // }
        // el.$router.push({ name: "main" });
        // return;
      }
    );
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
</style>
