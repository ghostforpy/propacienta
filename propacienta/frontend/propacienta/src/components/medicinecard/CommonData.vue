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
          <v-col cols="12" md="5">
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
            <v-select
              :items="[
                { gender: 'Мужской', abbr: 'male' },
                { gender: 'Женский', abbr: 'female' },
              ]"
              label="Пол"
              item-text="gender"
              item-value="abbr"
              v-model="gender"
              @change="updateHandl"
              color="cyan"
            ></v-select>
            <v-select
              :items="[
                { bloodType: 'O(I) Rh−', abbr: 'I−' },
                { bloodType: 'O(I) Rh+', abbr: 'I+' },
                { bloodType: 'A(II) Rh−', abbr: 'II−' },
                { bloodType: 'A(II) Rh+', abbr: 'II+' },
                { bloodType: 'B(III) Rh-', abbr: 'III' },
                { bloodType: 'B(III) Rh+', abbr: 'III+' },
                { bloodType: 'AB(IV) Rh−', abbr: 'IV−' },
                { bloodType: 'AB(IV) Rh+', abbr: 'IV+' },
              ]"
              label="Группа крови"
              item-text="bloodType"
              item-value="abbr"
              v-model="bloodType"
              @change="updateHandl"
              color="cyan"
            ></v-select>
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
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import TextFieldUserOwner from "@/components/users/TextFieldUserOwner";
import {
  MEDICINECARD_COMMON_GET,
  MEDICINECARD_COMMON_PATCH_REQUEST,
} from "@/store/actions/pacient";
export default {
  name: "OwnerMedicineCardCommonData",
  props: {
    pacientId: Number,
  },
  components: {
    TextFieldUserOwner,
  },
  data: function () {
    return {
      height: "",
      oldHeight: "",
      weight: "",
      oldWeight: "",
      gender: "",
      oldGender: "",
      bloodType: "",
      oldBloodType: "",
      applyBtn: false,
      loading: false,
      numberRules: [
        (value) => !!value || "Это поле является обязательным.",
        (value) => {
          const pattern = /^[1-2]?\d\d([.,]\d\d?)?$/g;
          return pattern.test(value) || "Неправильный формат.";
        },
      ],
    };
  },
  // watch: {
  //   height: function (val, oldVal) {
  //     console.log(val, oldVal);
  //   },
  //   weight: function (val, oldVal) {
  //     console.log(val, oldVal);
  //   },
  // },
  computed: {
    submitAvailable: function () {
      const v =
        this.height !== null &&
        this.height !== "" &&
        this.weight !== null &&
        this.weight !== "" &&
        this.$refs.height.$refs.field.valid &&
        this.$refs.weight.$refs.field.valid;
      return v;
    },
  },
  mounted: async function () {
    const res = await this.$store.dispatch(MEDICINECARD_COMMON_GET);
    if (res) {
      this.height = this.$store.getters.commondataResp.height;
      this.weight = this.$store.getters.commondataResp.weight;
      this.bloodType = this.$store.getters.commondataResp.blood_type;
      this.gender = this.$store.getters.commondataResp.gender;
      this.oldHeight = this.height;
      this.oldWeight = this.weight;
      this.oldBloodType = this.bloodType;
      this.oldGender = this.gender;
    }
  },
  methods: {
    updateHandl: function () {
      this.applyBtn = false;
      if (this.height !== this.oldHeight) {
        this.applyBtn = true;
      }
      if (this.weight !== this.oldWeight) {
        this.applyBtn = true;
      }
      if (this.gender !== this.oldGender) {
        this.applyBtn = true;
      }
      if (this.bloodType !== this.oldBloodType) {
        this.applyBtn = true;
      }
    },
    onSubmit: async function () {
      this.loading = true;
      let data = {
        height: this.height,
        weight: this.weight,
        gender: this.gender,
        blood_type: this.bloodType,
      };

      const res = await this.$store.dispatch(
        MEDICINECARD_COMMON_PATCH_REQUEST,
        data
      );
      this.loading = false;
      if (res) {
        this.applyBtn = false;
        this.oldHeight = this.height;
        this.oldWeight = this.weight;
        this.oldBloodType = this.bloodType;
        this.oldGender = this.gender;
      } else {
        console.log("wrong");
      }
    },
  },
};
</script>
