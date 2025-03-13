<template>
  <v-container>
    <SpinnerLoader v-if="issuesStore.loading" />
    <IssueCardDetailed v-if="issue" :issue="issue" />
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useIssuesStore } from '@/stores/issueStore';
import SpinnerLoader from '@/components/loader/SpinnerLoader.vue';
import IssueCardDetailed from '@/components/issue/IssueCardDetailed.vue';

const route = useRoute();
const issuesStore = useIssuesStore();
const issue = ref();

onMounted(async () => {
  const issueId = Number(route.params.id);
  try {
    issue.value = await issuesStore.fetchIssue(issueId);
  } catch (error) {
    console.error('Error loading issue:', error);
  }
});
</script>
