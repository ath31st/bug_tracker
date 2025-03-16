<template>
  <v-container>
    <v-card color="dark" class="pa-6 mt-4">
      <h3 class="mb-4">Оформление заявки</h3>
      <v-form @submit.prevent="submitIssue">
        <v-text-field
          variant="outlined"
          v-model="newIssue.title"
          label="Название"
          required
          clearable
        />
        <v-textarea
          variant="outlined"
          v-model="newIssue.description"
          label="Описание"
          required
          clearable
        />
        <v-select
          variant="outlined"
          v-model="newIssue.priority"
          :items="priorityOrder"
          :item-title="getPriorityName"
          :item-value="(self) => self"
          label="Приоритет"
          required
        />
        <CommonButton
          :disabled="
            !newIssue.title || !newIssue.description || !newIssue.priority
          "
          class="w-100"
          type="submit"
          variant="outlined"
        >
          Создать заявку
        </CommonButton>
      </v-form>

      <CommonSnackbar
        v-model="snackbarStore.isVisible"
        :message="snackbarStore.message"
        :timeout="snackbarStore.timeout"
        :color="snackbarStore.color"
      />
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useIssuesStore } from '@/stores/issueStore';
import { useSnackbarStore } from '@/stores/snackbarStore';
import CommonSnackbar from '@/components/CommonSnackbar.vue';
import type { NewIssue } from '@/types';
import CommonButton from '@/components/button/CommonButton.vue';
import { getPriorityName, priorityOrder } from '@/utils/priorityUtils';
import { useRouter } from 'vue-router';

const router = useRouter();
const issuesStore = useIssuesStore();
const snackbarStore = useSnackbarStore();

const newIssue = ref<NewIssue>({
  title: '',
  description: '',
  priority: 'MEDIUM',
});

const submitIssue = async () => {
  try {
    await issuesStore.createIssue(newIssue.value);

    router.push('/');
  } catch (error) {
    console.error('Ошибка при создании issue:', error);
    snackbarStore.show('Ошибка при создании заявки.', {
      color: 'error',
      timeout: 3000,
    });
  }
};
</script>
