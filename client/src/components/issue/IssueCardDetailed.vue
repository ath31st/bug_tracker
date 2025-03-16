<template>
  <v-card v-if="localIssue">
    <v-card-title class="headline">
      ID: {{ localIssue.id }} - {{ localIssue.title }}
    </v-card-title>
    <v-card-subtitle>
      <span>Создан: {{ formatDate(localIssue.createdAt) }}</span>
      <span
        v-if="
          !isEqualCreateAndUpdateDates(
            localIssue.createdAt,
            localIssue.updatedAt,
          )
        "
      >
        | Обновлен: {{ formatDate(localIssue.updatedAt) }}</span
      >
    </v-card-subtitle>
    <v-card-text>
      <v-row>
        <v-col cols="7">
          <p><strong>Описание:</strong></p>
          <p>{{ localIssue.description }}</p>
        </v-col>

        <v-divider vertical></v-divider>

        <v-col cols="5">
          <v-row>
            <v-col cols="6">
              <strong>Автор:</strong> {{ localIssue.reporter.username }}
            </v-col>
            <v-col cols="6">
              <strong>Статус:</strong>
              <v-chip :color="getStatusColor(localIssue.status)" class="ml-2">
                {{ getStatusName(localIssue.status) }}
              </v-chip>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <strong>Исполнитель:</strong>
              {{ localIssue.assignee?.username || 'Не назначен' }}
            </v-col>
            <v-col cols="6">
              <strong>Приоритет:</strong>
              <v-chip
                :color="getPriorityColor(localIssue.priority)"
                class="ml-2"
              >
                {{ getPriorityName(localIssue.priority) }}
              </v-chip>
            </v-col>
          </v-row>
          <v-row v-if="!localIssue.assignee && authUserId">
            <v-col cols="12" class="pt-2">
              <CommonButton
                variant="outlined"
                color="primary"
                class="w-100"
                @click="assignToMe"
              >
                Взять в работу
              </CommonButton>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-divider class="my-6"></v-divider>

      <CommentList
        :comments="localIssue.comments"
        :auth-user-id="authUserId"
        @delete="handleDeleteComment"
        @update="handleUpdateComment"
      />

      <v-row class="mt-2 mb-2" align="center">
        <v-col cols="10">
          <v-text-field
            v-model="comment"
            label="Добавить комментарий"
            variant="outlined"
            clearable
            density="compact"
            hide-details="auto"
          ></v-text-field>
        </v-col>
        <v-col cols="2">
          <CommonButton
            class="w-100"
            variant="outlined"
            color="white"
            :disabled="!comment || comment.trim() === ''"
            @click="submitComment"
          >
            Отправить
          </CommonButton>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
  <SpinnerLoader v-else />
</template>

<script setup lang="ts">
import { defineProps, ref, onMounted } from 'vue';
import { formatDate, isEqualCreateAndUpdateDates } from '@/utils/dateUtils';
import { getStatusColor, getStatusName } from '@/utils/statusUtils';
import { getPriorityColor, getPriorityName } from '@/utils/priorityUtils';
import type { Issue, NewComment, UpdateComment } from '@/types';
import CommentList from '@/components/comment/CommentList.vue';
import { useCommentsStore } from '@/stores/commentStore';
import { useAuthStore } from '@/stores/authStore';
import { useIssuesStore } from '@/stores/issueStore';
import CommonButton from '../button/CommonButton.vue';
import SpinnerLoader from '@/components/loader/SpinnerLoader.vue';

const commentsStore = useCommentsStore();
const issueStore = useIssuesStore();
const authStore = useAuthStore();

const props = defineProps<{
  issueId: number;
}>();

const localIssue = ref<Issue | null>(null);
const authUserId = ref(authStore.user?.id);
const comment = ref('');

onMounted(async () => {
  await loadIssue();
});

async function loadIssue() {
  try {
    const issue = await issueStore.fetchIssue(props.issueId);
    localIssue.value = issue;
  } catch (err) {
    console.error('Ошибка при загрузке задачи:', err);
  }
}

const submitComment = async () => {
  if (
    !comment.value ||
    comment.value.trim() === '' ||
    commentsStore.loading ||
    !localIssue.value
  )
    return;

  const newComment: NewComment = {
    content: comment.value.trim(),
    issueId: localIssue.value.id,
  };

  try {
    await commentsStore.createComment(newComment);
    const updatedComments = await commentsStore.getCommentsByIssueId(
      localIssue.value.id,
    );
    localIssue.value.comments = updatedComments;
  } catch (err) {
    console.error(err);
  } finally {
    comment.value = '';
  }
};

const handleUpdateComment = async (
  commentId: number,
  comment: UpdateComment,
) => {
  try {
    await commentsStore.updateComment(commentId, comment);
    const updatedComment = await commentsStore.getCommentById(commentId);
    const index = localIssue.value!.comments.findIndex(
      (c) => c.id === commentId,
    );
    if (index !== -1) localIssue.value!.comments[index] = updatedComment;
  } catch (err) {
    console.error(err);
  }
};

const handleDeleteComment = async (commentId: number) => {
  try {
    await commentsStore.deleteComment(commentId);
    localIssue.value!.comments = localIssue.value!.comments.filter(
      (c) => c.id !== commentId,
    );
  } catch (err) {
    console.error(err);
  }
};

const assignToMe = async () => {
  if (!localIssue.value) return;

  try {
    const updatedIssue = await issueStore.assignIssue(localIssue.value.id);
    localIssue.value = updatedIssue;
  } catch (err) {
    console.error('Ошибка при назначении задачи:', err);
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
