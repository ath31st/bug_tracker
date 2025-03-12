<template>
  <v-app-bar app color="primary">
    <v-toolbar-title>
      <router-link to="/" class="text-decoration-none white--text">
        Bug tracker
      </router-link>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn text to="/" exact>Home</v-btn>
    <v-btn text to="/about">About</v-btn>

    <template v-if="authStore.user">
      <v-btn text @click="logout">Logout</v-btn>
      <v-chip color="white" text-color="primary" class="ml-2">
        {{ authStore.user?.username.toUpperCase() || 'User' }}
      </v-chip>
    </template>
    <template v-else>
      <v-btn text to="/login">Login</v-btn>
    </template>
  </v-app-bar>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

function logout() {
  authStore.logout();
  router.push('/login');
}
</script>

<style scoped></style>
