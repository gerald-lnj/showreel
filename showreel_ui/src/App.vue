<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-toolbar-title>Reel Maker</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <Main/>

    </v-main>
  </v-app>
</template>

<script>
import Main from './components/Main';

export default {
  name: 'App',

  components: {
    Main,
  },

  data: () => ({
    //
  }),
};
</script>
