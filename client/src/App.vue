<template>
  <v-app
    :style="{
      backgroundImage: `url(${backgroundImage})`,
      backgroundRepeat: 'no-repeat',
      backgroundPosition: 'center center',
      backgroundAttachment: 'fixed',
      backgroundSize: 'cover',
      minHeight: '100vh',
    }"
  >
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
import backgroundImage from '@/assets/background.jpg';

const route = useRoute();
const noLayoutRoutes = ['/login', '/register', '/not-found'];

const shouldShowLayout = computed(() => {
  return !noLayoutRoutes.includes(route.path);
});
</script>
