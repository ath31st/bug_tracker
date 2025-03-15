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

      <v-row class="mt-2" align="center">
        <v-col cols="10">
          <v-text-field
            v-model="comment"
            label="Добавить комментарий"
            variant="outlined"
            clearable
            hide-details="auto"
          ></v-text-field>
        </v-col>
        <v-col cols="2">
          <v-btn
            color="primary"
            :disabled="!comment || comment.trim() === ''"
            @click="submitComment"
          >
            Отправить
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { defineProps, reactive, ref } from 'vue';
import { formatDate } from '@/utils/formatDate';
import { getStatusColor, getStatusName } from '@/utils/statusUtils';
import { getPriorityColor, getPriorityName } from '@/utils/priorityUtils';
import type { Issue, NewComment, Comment } from '@/types';
import CommentList from '@/components/comment/CommentList.vue';
import { useCommentsStore } from '@/stores/commentStore';

const commentsStore = useCommentsStore();

const props = defineProps<{
  issue: Issue;
}>();

const comment = ref('');
const localComments = reactive<Comment[]>(props.issue.comments);

const submitComment = async () => {
  if (!comment.value || comment.value.trim() === '' || commentsStore.loading)
    return;

  const newComment: NewComment = {
    content: comment.value.trim(),
    issueId: props.issue.id,
  };

  try {
    await commentsStore.createComment(newComment);
    const updatedComments = await commentsStore.getCommentsByIssueId(
      props.issue.id,
    );

    localComments.splice(0, localComments.length, ...updatedComments);
  } catch (err) {
    console.error(err);
  } finally {
    comment.value = '';
  }
};
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
