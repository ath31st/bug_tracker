<template>
  <v-container>
    <IssueCardDetailed :issueId="issueId" />
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import IssueCardDetailed from '@/components/issue/IssueCardDetailed.vue';

const route = useRoute();
const issueId = ref(Number(route.params.id));
</script>
