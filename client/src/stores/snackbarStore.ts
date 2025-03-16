import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSnackbarStore = defineStore('snackbar', () => {
  const isVisible = ref(false);
  const message = ref('');
  const color = ref('grey');
  const timeout = ref(3000);

  const show = (
    msg: string,
    options: { color?: string; timeout?: number } = {},
  ) => {
    message.value = msg;
    color.value = options.color || 'grey';
    timeout.value = options.timeout || 3000;
    isVisible.value = true;
  };

  const hide = () => {
    isVisible.value = false;
  };

  return {
    isVisible,
    message,
    color,
    timeout,
    show,
    hide,
  };
});
