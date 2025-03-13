<template>
  <v-card>
    <v-card-title class="headline">
      ID: {{ issue.id }} - {{ issue.title }}
    </v-card-title>
    <v-card-subtitle>
      Создан: {{ formatDate(issue.createdAt) }} | Обновлен:
      {{ formatDate(issue.updatedAt) }}
    </v-card-subtitle>
    <v-card-text>
      <v-row>
        <v-col cols="7">
          <p><strong>Описание:</strong></p>
          <p>{{ issue.description }}</p>
        </v-col>

        <v-divider vertical></v-divider>

        <v-col cols="5">
          <v-row>
            <v-col cols="6">
              <strong>Автор:</strong> {{ issue.reporter.username }}
            </v-col>
            <v-col cols="6">
              <strong>Статус:</strong>
              <v-chip :color="getStatusColor(issue.status)" class="ml-2">
                {{ getStatusName(issue.status) }}
              </v-chip>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <strong>Исполнитель:</strong>
              {{ issue.assignee?.username || 'Не назначен' }}
            </v-col>

            <v-col cols="6">
              <strong>Приоритет:</strong>
              <v-chip :color="getPriorityColor(issue.priority)" class="ml-2">
                {{ getPriorityName(issue.priority) }}
              </v-chip>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-divider class="my-6"></v-divider>

      <CommentList :comments="issue.comments" />
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { formatDate } from '@/utils/formatDate';
import { getStatusColor, getStatusName } from '@/utils/statusUtils';
import { getPriorityColor, getPriorityName } from '@/utils/priorityUtils';
import type { Issue } from '@/types';
import CommentList from '@/components/comment/CommentList.vue';

defineProps<{
  issue: Issue;
}>();
</script>

<style scoped>
.headline {
  font-size: 1.5rem;
  font-weight: bold;
}

.v-card-subtitle {
  margin-top: 8px;
}
</style>
