<template>
  <v-dialog
    v-model="dialogVisible"
    max-width="400px"
    @update:model-value="onDialogUpdate"
  >
    <v-card>
      <v-card-title class="headline text-center"
        >Информация о пользователе</v-card-title
      >
      <v-card-text>
        <v-row v-if="user">
          <v-col>
            <div><strong>Логин:</strong> {{ user.username }}</div>
            <div><strong>E-mail:</strong> {{ user.email }}</div>
            <div>
              <strong>Дата регистрации:</strong>
              {{ formatDate(user.createdAt) }}
            </div>
          </v-col>
        </v-row>
        <v-row v-else>
          <v-col>Данные пользователя отсутствуют</v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <CommonButton class="w-100" variant="outlined" @click="emitClose">
          Закрыть
        </CommonButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { User } from '@/types';
import { formatDate } from '@/utils/dateUtils';
import CommonButton from '../common/CommonButton.vue';

const props = defineProps<{
  user: User | null;
  visible: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => {
    if (!value) emit('close');
  },
});

const onDialogUpdate = (value: boolean) => {
  if (!value) emit('close');
};

const emitClose = () => {
  emit('close');
};
</script>

<style scoped></style>
