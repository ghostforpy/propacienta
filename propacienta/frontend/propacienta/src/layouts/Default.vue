<template>
  <div>
    <v-app-bar app color="blue">
      <v-app-bar-title>
        <router-link class="link" to="/">Propacienta</router-link>
      </v-app-bar-title>
    </v-app-bar>
    <section class="content">
      <!--Элемент, который при отрисовке будет заменен на ваш view-->
      <slot />
    </section>
    <footer></footer>
  </div>
</template>




<script>
export default {
  name: "DefaultLayout",
};
</script>