<template>
  <v-card-actions>
    <v-row justify="start">
      <v-col cols="2">
        <CommonButton class="w-100" variant="outlined" to="/new-issue">
          <v-icon>mdi-bug</v-icon>
          Создать заявку
        </CommonButton>
      </v-col>
      <v-col cols="2">
        <CommonButton
          class="w-100"
          :variant="filterMyIssues ? 'elevated' : 'outlined'"
          @click="toggleMyIssues"
        >
          <v-icon>mdi-account</v-icon>
          Мои заявки
        </CommonButton>
      </v-col>
      <v-col cols="2">
        <CommonButton
          class="w-100"
          :variant="filterAssignedToMe ? 'elevated' : 'outlined'"
          @click="toggleAssignedToMe"
        >
          <v-icon>mdi-account-check</v-icon>
          Приняты в работу
        </CommonButton>
      </v-col>
    </v-row>
  </v-card-actions>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import CommonButton from '@/components/button/CommonButton.vue';
import { useIssuesStore } from '@/stores/issueStore';
import { useAuthStore } from '@/stores/authStore';

const issuesStore = useIssuesStore();
const authStore = useAuthStore();

const filterMyIssues = ref(false);
const filterAssignedToMe = ref(false);
const currentUserId = authStore.user?.id;

const toggleMyIssues = async () => {
  filterMyIssues.value = !filterMyIssues.value;
  filterAssignedToMe.value = false;
  await applyFilters();
};

const toggleAssignedToMe = async () => {
  filterAssignedToMe.value = !filterAssignedToMe.value;
  filterMyIssues.value = false;
  await applyFilters();
};

const applyFilters = async () => {
  const reporterId = filterMyIssues.value ? currentUserId : undefined;
  const assigneeId = filterAssignedToMe.value ? currentUserId : undefined;
  await issuesStore.setFilters(reporterId, assigneeId);
  await issuesStore.fetchIssues();
};
</script>

<style scoped></style>
