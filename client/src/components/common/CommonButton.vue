<template>
  <v-btn
    :color="color"
    :variant="variant"
    :loading="loading"
    :disabled="disabled"
    class="custom-btn"
    :type="type"
    @click="$emit('click', $event)"
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
  type?: 'button' | 'submit' | 'reset';
}>();

defineEmits<{
  (e: 'click', event: Event): void;
}>();
</script>

<style scoped>
.custom-btn {
  text-transform: none;
}

.custom-btn:disabled {
  opacity: 0.4;
}
</style>
