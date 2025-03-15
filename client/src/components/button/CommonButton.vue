<template>
  <v-btn
    :color="color"
    :variant="variant"
    :loading="loading"
    :disabled="disabled"
    class="custom-btn"
    @click="$emit('click')"
  >
    <slot />
  </v-btn>
</template>

<script setup lang="ts">
defineProps<{
  color?: string;
  variant?: 'flat' | 'outlined' | 'text' | 'elevated' | 'tonal';
  loading?: boolean;
  disabled?: boolean;
}>();
</script>

<style scoped>
.custom-btn {
  text-transform: none;
}
</style>
