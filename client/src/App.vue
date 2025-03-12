<template>
  <v-app>
    <HeaderComponent v-if="shouldShowLayout" />
    <v-main>
      <router-view />
    </v-main>
    <FooterComponent v-if="shouldShowLayout" />
  </v-app>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import HeaderComponent from '@/components/HeaderComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';

const route = useRoute();
const noLayoutRoutes = ['/login', '/register'];

const shouldShowLayout = computed(() => {
  return !noLayoutRoutes.includes(route.path);
});
</script>
