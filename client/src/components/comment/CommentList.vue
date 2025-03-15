<template>
  <div>
    <h3>Комментарии</h3>

    <v-list v-if="comments.length">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :is-author="authUserId === comment.author.id"
        @update="
          ($event, updatedComment) => $emit('update', $event, updatedComment)
        "
        @delete="($event) => $emit('delete', $event)"
      />
    </v-list>

    <v-alert v-else type="info" class="mt-2">Комментариев пока нет</v-alert>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import type { Comment, UpdateComment } from '@/types';
import CommentItem from './CommentItem.vue';

defineProps<{
  comments: Comment[];
  authUserId?: number;
}>();

defineEmits<{
  (e: 'delete', id: number): void;
  (e: 'update', id: number, comment: UpdateComment): void;
}>();
</script>

<style scoped></style>
