<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm6 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="cyan darken-1">
            <v-toolbar-title
              >Запрашиваемая страница не найдена.</v-toolbar-title
            >
          </v-toolbar>
          <v-card-text> Ошибка 404. </v-card-text>
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
  name: "NotFound",
};
</script>

<style></style>
