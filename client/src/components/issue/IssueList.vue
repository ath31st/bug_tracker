<template>
  <v-row>
    <v-col cols="12" v-for="issue in issues" :key="issue.id">
      <router-link :to="`/issue/${issue.id}`" class="issue-link">
        <IssueCardSmall :issue="issue" />
      </router-link>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import IssueCardSmall from '@/components/issue/IssueCard.vue';
import type { Issue } from '@/types';

defineProps<{
  issues: Issue[];
}>();
</script>

<style scoped>
.issue-link {
  text-decoration: none;
}

.issue-link:hover .v-card {
  background-color: rgb(var(--v-theme-primary));
  transition: background-color 0.2s ease;
}
</style>
