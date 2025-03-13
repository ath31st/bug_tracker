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
        <v-col cols="12" md="6">
          <p><strong>Описание:</strong></p>
          <p>{{ issue.description }}</p>
        </v-col>
        <v-col cols="12" md="6">
          <v-row>
            <v-col cols="6">
              <strong>Статус:</strong>
              <v-chip :color="getStatusColor(issue.status)" class="ml-2">
                {{ getStatusName(issue.status) }}
              </v-chip>
            </v-col>
            <v-col cols="6">
              <strong>Приоритет:</strong>
              <v-chip :color="getPriorityColor(issue.priority)" class="ml-2">
                {{ issue.priority }}
              </v-chip>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <strong>Автор:</strong> {{ issue.reporter.username }}
            </v-col>
            <v-col cols="6">
              <strong>Исполнитель:</strong>
              {{ issue.assignee?.username || 'Не назначен' }}
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { formatDate } from '@/utils/formatDate';
import { getStatusColor, getStatusName } from '@/utils/statusUtils';
import { getPriorityColor } from '@/utils/priorityUtils';
import type { Issue } from '@/types';

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
