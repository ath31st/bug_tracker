<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-6 pa-4">
          <v-card-title class="text-h5 d-flex align-center justify-center">
            <v-icon>mdi-bug</v-icon>
            Вход в Bug tracker
          </v-card-title>

          <v-card-subtitle class="text-center mt-2">
            Введите логин и пароль для входа
          </v-card-subtitle>

          <v-card-text>
            <v-form @submit.prevent="login" ref="form" v-model="valid">
              <v-text-field
                v-model="credentials.username"
                label="Логин"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :rules="[rules.required]"
                class="mb-4"
              />
              <v-text-field
                v-model="credentials.password"
                label="Пароль"
                prepend-inner-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                :rules="[rules.required]"
              />
              <v-card-actions class="d-flex flex-column justify-center">
                <CommonButton
                  class="w-100"
                  color="white"
                  large
                  :loading="loading"
                  :disabled="!valid"
                  type="submit"
                >
                  Войти
                </CommonButton>
                <CommonButton class="w-100" text to="/register" color="white">
                  Нет аккаунта? Зарегистрируйтесь
                </CommonButton>
              </v-card-actions>
            </v-form>
          </v-card-text>

          <CommonSnackbar
            v-model="snackbarStore.isVisible"
            :message="snackbarStore.message"
            :timeout="snackbarStore.timeout"
            :color="snackbarStore.color"
          />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useSnackbarStore } from '@/stores/snackbarStore';
import CommonButton from '@/components/button/CommonButton.vue';
import CommonSnackbar from '@/components/CommonSnackbar.vue';

const router = useRouter();
const authStore = useAuthStore();
const snackbarStore = useSnackbarStore();
const form = ref(null);
const valid = ref(false);
const loading = ref(false);

const credentials = ref({
  username: '',
  password: '',
});

const showPassword = ref(false);

const rules = {
  required: (value: string) => !!value || 'Поле обязательно',
};

const login = async () => {
  try {
    loading.value = true;
    await authStore.loginUser(credentials.value);
    router.push('/');
  } catch (error: unknown) {
    console.error(error);
    snackbarStore.show('Ошибка входа. Проверьте данные.', {
      color: 'error',
      timeout: 3000,
    });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.v-btn {
  transition: all 0.3s ease;
}
</style>
