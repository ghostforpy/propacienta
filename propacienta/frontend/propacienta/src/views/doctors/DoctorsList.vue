<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm6 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="cyan darken-1">
            <v-toolbar-title>Страница списка врачей</v-toolbar-title>
          </v-toolbar>
          <v-card-text> Осталось придумать контент) </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              class="white-content"
              color="cyan"
              :to="{ name: 'main' }"
              block
            >
              Ok</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: "DoctorsList",
};
</script>

<style></style>
