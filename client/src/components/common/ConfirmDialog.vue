<template>
  <v-dialog v-model="dialog" max-width="400">
    <v-card>
      <v-card-title class="headline text-center">{{ title }}</v-card-title>
      <v-card-text>{{ message }}</v-card-text>
      <v-card-actions class="justify-end">
        <CommonButton
          class="w-100"
          variant="outlined"
          :color="cancelColor"
          @click="emitConfirm"
        >
          {{ confirmText }}
        </CommonButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import CommonButton from '../common/CommonButton.vue';

const props = defineProps<{
  modelValue: boolean;
  title?: string;
  message?: string;
  confirmText?: string;
  cancelText?: string;
  confirmColor?: string;
  cancelColor?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
  (e: 'confirm'): void;
}>();

const dialog = ref(props.modelValue);

watch(
  () => props.modelValue,
  (newValue) => {
    dialog.value = newValue;
  },
);

watch(dialog, (newValue) => {
  emit('update:modelValue', newValue);
});

const emitConfirm = () => {
  emit('confirm');
  dialog.value = false;
};
</script>
