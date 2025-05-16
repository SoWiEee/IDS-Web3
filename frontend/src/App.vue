<template>
  <v-app>
    <!-- nav bar -->
    <v-app-bar color="primary" dark>
      <v-toolbar-title>Security Monitoring</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/" text> Main </v-btn>
      <v-btn to="/malicious" text> Malicious Record </v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>

</script>