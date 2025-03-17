<template>
  <v-snackbar v-model="isVisible" :timeout="timeout" :color="color" top>
    {{ message }}
    <template v-slot:actions>
      <v-btn text @click="isVisible = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  message: string;
  timeout?: number;
  color?: string;
  modelValue: boolean;
}>();

const emit = defineEmits(['update:modelValue']);

const isVisible = ref(false);

watch(
  () => isVisible.value,
  (newValue) => {
    emit('update:modelValue', newValue);
  },
);

watch(
  () => props.modelValue,
  (newValue) => {
    isVisible.value = newValue;
  },
);
</script>
