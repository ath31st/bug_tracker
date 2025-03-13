<template>
  <div>
    <h3>Комментарии</h3>

    <v-list v-if="comments.length">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
    </v-list>

    <v-alert v-else type="info" class="mt-2">Комментариев пока нет</v-alert>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import type { Comment } from '@/types';

defineProps<{
  comments: Comment[];
}>();
</script>

<style scoped>
.comment-date {
  font-size: 0.8rem;
  color: gray;
  margin-left: 8px;
}
</style>
