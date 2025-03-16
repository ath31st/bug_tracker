<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-6 pa-4">
          <v-card-title class="text-h5 d-flex align-center justify-center">
            <v-icon>mdi-bug</v-icon>
            Регистрация в Bug tracker
          </v-card-title>

          <v-card-subtitle class="text-center mt-2">
            Заполните данные для регистрации
          </v-card-subtitle>

          <v-card-text>
            <v-form @submit.prevent="register" ref="form" v-model="valid">
              <v-text-field
                v-model="credentials.username"
                label="Логин"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :rules="[rules.required]"
                class="mb-4"
              />
              <v-text-field
                v-model="credentials.email"
                label="E-mail"
                prepend-inner-icon="mdi-mail"
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
                :rules="[rules.required, rules.minLength]"
              />
              <v-text-field
                v-model="credentials.confirmPassword"
                label="Подтверждение пароля"
                prepend-inner-icon="mdi-lock-check"
                :type="showConfirmPassword ? 'text' : 'password'"
                :append-inner-icon="
                  showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'
                "
                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                variant="outlined"
                :rules="[rules.required, rules.matchPassword]"
              />
            </v-form>
          </v-card-text>

          <v-card-actions class="d-flex justify-center">
            <CommonButton
              color="white"
              large
              :loading="loading"
              :disabled="!valid"
              @click="register"
            >
              Зарегистрироваться
            </CommonButton>
          </v-card-actions>

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
import { useUsersStore } from '@/stores/userStore';
import CommonButton from '@/components/button/CommonButton.vue';
import { useSnackbarStore } from '@/stores/snackbarStore';
import CommonSnackbar from '@/components/CommonSnackbar.vue';
import type { NewUser } from '@/types';

const router = useRouter();
const authStore = useAuthStore();
const userStore = useUsersStore();
const snackbarStore = useSnackbarStore();

const form = ref(null);
const valid = ref(false);
const loading = ref(false);

const credentials = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);

const rules = {
  required: (value: string) => !!value || 'Поле обязательно',
  minLength: (value: string) => value.length >= 4 || 'Минимум 4 символов',
  matchPassword: (value: string) =>
    value === credentials.value.password || 'Пароли не совпадают',
};

const register = async () => {
  try {
    loading.value = true;

    const newUser: NewUser = {
      username: credentials.value.username,
      email: credentials.value.email,
      password: credentials.value.password,
    };

    await userStore.createUser(newUser);
    await authStore.loginUser({
      username: credentials.value.username,
      password: credentials.value.password,
    });

    snackbarStore.show('Регистрация выполнена успешно!', {
      color: 'success',
      timeout: 2000,
    });

    await new Promise((resolve) => setTimeout(resolve, 1000));

    router.push('/');
  } catch (error: unknown) {
    console.error(error);

    snackbarStore.show('Ошибка регистрации. Проверьте данные.', {
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
