<template>
  <v-card-subtitle>
    <span>Создан: {{ formatDate(createdAt) }}</span>
    <span v-if="!isEqualCreateAndUpdateDates(createdAt, updatedAt)">
      | Обновлен: {{ formatDate(updatedAt) }}</span
    >
  </v-card-subtitle>
</template>

<script setup lang="ts">
import { formatDate, isEqualCreateAndUpdateDates } from '@/utils/dateUtils';

defineProps<{ createdAt: string; updatedAt: string }>();
</script>
