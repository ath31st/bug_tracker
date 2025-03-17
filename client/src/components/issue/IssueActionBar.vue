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
          :variant="isMyIssuesActive ? 'elevated' : 'outlined'"
          @click="toggleMyIssues"
        >
          <v-icon>mdi-account</v-icon>
          Мои заявки
        </CommonButton>
      </v-col>
      <v-col cols="2">
        <CommonButton
          class="w-100"
          :variant="isAssignedToMeActive ? 'elevated' : 'outlined'"
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
import { computed } from 'vue';
import CommonButton from '@/components/common/CommonButton.vue';
import { useIssuesStore } from '@/stores/issueStore';
import { useAuthStore } from '@/stores/authStore';

const issuesStore = useIssuesStore();
const authStore = useAuthStore();

const currentUserId = authStore.user?.id;

const isMyIssuesActive = computed(
  () => issuesStore.filterReporterId === currentUserId,
);
const isAssignedToMeActive = computed(
  () => issuesStore.filterAssigneeId === currentUserId,
);

const toggleMyIssues = async () => {
  const newReporterId = isMyIssuesActive.value ? undefined : currentUserId;
  await issuesStore.setFilters(newReporterId, undefined);
  await issuesStore.fetchIssues();
};

const toggleAssignedToMe = async () => {
  const newAssigneeId = isAssignedToMeActive.value ? undefined : currentUserId;
  await issuesStore.setFilters(undefined, newAssigneeId);
  await issuesStore.fetchIssues();
};
</script>

<style scoped></style>
