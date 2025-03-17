<template>
  <v-container>
    <IssueActionBar
      :is-my-issues-active="isMyIssuesActive"
      :is-assigned-to-me-active="isAssignedToMeActive"
      @toggle-my-issues="toggleMyIssues"
      @toggle-assigned-to-me="toggleAssignedToMe"
    />
    <IssueListHeader @sort="handleSort" />
    <SpinnerLoader v-if="issuesStore.loading" />

    <v-alert v-if="issuesStore.error" type="error" dismissible class="my-4">
      {{ issuesStore.error }}
    </v-alert>

    <IssueList
      :issues="issuesStore.issues"
      v-if="!issuesStore.loading && issuesStore.issues.length"
    />

    <v-alert
      v-if="
        !issuesStore.loading && !issuesStore.issues.length && !issuesStore.error
      "
      type="info"
      class="my-4"
    >
      Заявок пока нет
    </v-alert>

    <div class="pagination-controls" v-if="issuesStore.totalPages > 1">
      <v-row align="center" class="my-4">
        <v-col cols="2">
          <v-select
            variant="outlined"
            v-model="itemsPerPage"
            :items="[5, 10, 20, 50]"
            label="Эл. на странице"
            @update:modelValue="handleItemsPerPageChange"
          />
        </v-col>
        <v-col cols="8">
          <v-pagination
            v-model="issuesStore.currentPage"
            :length="issuesStore.totalPages"
            :total-visible="7"
            @update:modelValue="handlePageChange"
          />
        </v-col>
        <v-col cols="2" class="text-right">
          <span>
            Показано {{ startIndex }}-{{ endIndex }} из
            {{ issuesStore.totalItems }}
          </span>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useIssuesStore } from '@/stores/issueStore';
import IssueListHeader from '@/components/issue/IssueListHeader.vue';
import SpinnerLoader from '@/components/common/SpinnerLoader.vue';
import IssueList from '@/components/issue/IssueList.vue';
import IssueActionBar from '@/components/issue/IssueActionBar.vue';
import { useAuthStore } from '@/stores/authStore';

const issuesStore = useIssuesStore();
const authStore = useAuthStore();

const itemsPerPage = ref(issuesStore.elementsPerPage);

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

const startIndex = computed(() => {
  return (issuesStore.currentPage - 1) * issuesStore.elementsPerPage + 1;
});

const endIndex = computed(() => {
  const end = issuesStore.currentPage * issuesStore.elementsPerPage;
  return end > issuesStore.totalItems ? issuesStore.totalItems : end;
});

const handlePageChange = async (page: number) => {
  try {
    await issuesStore.setPage(page);
  } catch (error) {
    console.error('Error changing page:', error);
  }
};

const handleItemsPerPageChange = async (value: number) => {
  try {
    issuesStore.elementsPerPage = value;
    await issuesStore.setElementsPerPage(value);
  } catch (error) {
    console.error('Error changing items per page:', error);
  }
};

const handleSort = async (sortData: {
  key: string;
  direction: 'asc' | 'desc';
}) => {
  try {
    await issuesStore.setSort(sortData.key, sortData.direction);
    await issuesStore.fetchIssues();
  } catch (error) {
    console.error('Error sorting:', error);
  }
};

onMounted(async () => {
  try {
    await issuesStore.fetchIssues();
  } catch (error) {
    console.error('Error loading issues:', error);
  }
});
</script>

<style scoped>
.pagination-controls {
  margin-top: 10px;
}

.issue-link {
  text-decoration: none;
}

.issue-link:hover .v-card {
  background-color: var(--v-primary-base);
  transition: background-color 0.2s ease;
}
</style>
