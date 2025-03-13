<template>
  <v-app-bar app color="primary">
    <v-toolbar-title>
      <h3>Bug tracker</h3>
    </v-toolbar-title>
    <v-spacer></v-spacer>

    <div class="d-flex">
      <v-btn text to="/" exact>Главная</v-btn>
      <v-btn text to="/about">О проекте</v-btn>

      <template v-if="authStore.user">
        <v-btn text @click="logout">Выход</v-btn>
        <v-chip size="large" class="ml-2 mr-10">
          {{ authStore.user?.username.toUpperCase() || 'User' }}
        </v-chip>
      </template>
    </div>
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

<style scoped>
.d-flex > * {
  margin-right: 16px;
}
.v-btn {
  width: 100px;
}
</style>
