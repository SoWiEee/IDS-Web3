<template>
  <v-app>
    <!-- nav bar -->
    <v-app-bar color="primary" dark>
      <v-toolbar-title class="title-text">Security Monitoring</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn
        to="/"
        class="custom-nav-btn"
        exact
        @mouseover="hoveredBtn = 'main'"
        @mouseleave="hoveredBtn = null"
      >
        <v-icon class="mr-1">mdi-home</v-icon>
        Main
        <div v-if="hoveredBtn === 'main'" class="shimmer"></div>
      </v-btn>

      <v-btn
        to="/malicious"
        class="custom-nav-btn"
        @mouseover="hoveredBtn = 'malicious'"
        @mouseleave="hoveredBtn = null"
      >
        <v-icon class="mr-1">mdi-alert</v-icon>
        Malicious Record
        <div v-if="hoveredBtn === 'malicious'" class="shimmer"></div>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
const hoveredBtn = ref(null)
</script>

<style scoped>
.title-text {
  font-size: 24px;
  font-weight: bold;
}

.custom-nav-btn {
  position: relative;
  overflow: hidden;
  background-color: #1e1e1e;
  color: #4CAF50 !important;
  border-radius: 20px;
  padding: 10px 20px;
  margin-left: 10px;
  font-weight: bold;
  font-size: 16px;
  text-transform: none;
  transition: all 0.3s;
}

.custom-nav-btn:hover {
  background-color: #333333;
}

.router-link-exact-active.custom-nav-btn {
  box-shadow: 0 4px 12px rgba(0, 255, 0, 0.4);
  background-color: #2e2e2e;
}

.shimmer {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmer-move 0.8s linear infinite;
  pointer-events: none;
}

@keyframes shimmer-move {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}
</style>
