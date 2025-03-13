<template>
  <v-container>
    <IssueListHeader />

    <SpinnerLoader v-if="issuesStore.loading" />

    <v-alert v-if="issuesStore.error" type="error" dismissible class="my-4">
      {{ issuesStore.error }}
    </v-alert>

    <v-row v-if="!issuesStore.loading && issuesStore.issues.length">
      <v-col cols="12" v-for="issue in issuesStore.issues" :key="issue.id">
        <router-link :to="`/issue/${issue.id}`" class="issue-link">
          <IssueCardSmall :issue="issue" />
        </router-link>
      </v-col>
    </v-row>

    <v-alert
      v-if="
        !issuesStore.loading && !issuesStore.issues.length && !issuesStore.error
      "
      type="info"
      class="my-4"
    >
      No issues found
    </v-alert>

    <div class="pagination-controls" v-if="issuesStore.totalPages > 1">
      <v-row align="center" class="my-4">
        <v-col cols="2">
          <v-select
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
import IssueCardSmall from '@/components/issue/IssueCard.vue';
import SpinnerLoader from '@/components/loader/SpinnerLoader.vue';

const issuesStore = useIssuesStore();
const itemsPerPage = ref(issuesStore.elementsPerPage);

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
