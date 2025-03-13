<template>
  <v-list-item>
    <v-list-item-title>
      <strong>{{ comment.author.username }}</strong>
      <span class="comment-date">{{ formatDate(comment.createdAt) }}</span>
    </v-list-item-title>
    <v-list-item-subtitle>{{ comment.content }}</v-list-item-subtitle>
  </v-list-item>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { formatDate } from '@/utils/formatDate';
import type { Comment } from '@/types';

defineProps<{
  comment: Comment;
}>();
</script>

<style scoped>
.comment-date {
  font-size: 0.8rem;
  color: gray;
  margin-left: 8px;
}
</style>
