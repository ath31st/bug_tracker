<template>
  <v-card>
    <v-card-text>
      <v-row align="center">
        <v-col cols="1">
          <span class="font-weight-bold">#{{ issue.id }}</span>
        </v-col>
        <v-col cols="2">
          <span>{{ issue.title }}</span>
        </v-col>
        <v-col cols="1">
          <v-chip :color="getStatusColor(issue.status)" size="small">
            {{ getStatusName(issue.status) }}
          </v-chip>
        </v-col>
        <v-col cols="1">
          <v-chip :color="getPriorityColor(issue.priority)" size="small">
            <v-icon small>{{ getPriorityIcon(issue.priority) }}</v-icon>
            <v-tooltip activator="parent" location="top">
              {{ getPriorityName(issue.priority) }}
            </v-tooltip>
          </v-chip>
        </v-col>
        <v-col cols="2">
          <span>{{ issue.reporter.username }}</span>
        </v-col>
        <v-col cols="2">
          <span>{{ issue.assignee?.username || '-' }}</span>
        </v-col>
        <v-col cols="3">
          <span>{{ formatDate(issue.createdAt) }}</span>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import type { Issue } from '@/types';
import { formatDate } from '@/utils/dateUtils';
import { getStatusColor, getStatusName } from '@/utils/statusUtils';
import {
  getPriorityColor,
  getPriorityName,
  getPriorityIcon,
} from '@/utils/priorityUtils';

defineProps<{
  issue: Issue;
}>();
</script>

<style scoped>
.v-col {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
