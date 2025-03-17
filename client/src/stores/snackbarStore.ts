import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSnackbarStore = defineStore('snackbar', () => {
  const isVisible = ref(false);
  const message = ref('');
  const color = ref('grey');
  const timeout = ref(3000);
  const timer = ref<number | null>(null);

  const show = (
    msg: string,
    options: { color?: string; timeout?: number } = {},
  ) => {
    if (timer.value !== null) {
      clearTimeout(timer.value);
    }

    message.value = msg;
    color.value = options.color || 'grey';
    timeout.value = options.timeout || 3000;
    isVisible.value = true;

    timer.value = setTimeout(() => {
      hide();
    }, timeout.value);
  };

  const hide = () => {
    isVisible.value = false;
    if (timer.value !== null) {
      clearTimeout(timer.value);
      timer.value = null;
    }
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
