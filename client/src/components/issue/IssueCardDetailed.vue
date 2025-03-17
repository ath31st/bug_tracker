<template>
  <v-card v-if="localIssue" class="pa-2">
    <v-card-title class="headline">
      <IssueHeader
        :issue-id="localIssue.id"
        :title="localIssue.title"
        :reporter-id="localIssue.reporter.id"
        :auth-user-id="authUserId"
        :is-editing="isEditing"
        @update:title="editedIssue.title = $event"
      >
        <template #actions>
          <IssueActions
            :auth-user-id="authUserId"
            :reporter-id="localIssue.reporter.id"
            :assignee-id="localIssue.assignee?.id"
            :is-editing="isEditing"
            @start-editing="startEditing"
            @save-changes="saveChanges"
            @cancel-editing="cancelEditing"
          />
        </template>
      </IssueHeader>
    </v-card-title>

    <IssueDates
      :created-at="localIssue.createdAt"
      :updated-at="localIssue.updatedAt"
    />

    <v-card-text>
      <IssueDetails
        :description="localIssue.description"
        :status="localIssue.status"
        :priority="localIssue.priority"
        :reporter-username="localIssue.reporter.username"
        :assignee-username="localIssue.assignee?.username"
        :reporter-id="localIssue.reporter.id"
        :auth-user-id="authUserId"
        :is-editing="isEditing"
        @update:description="editedIssue.description = $event"
        @update:status="editedIssue.status = $event"
        @update:priority="editedIssue.priority = $event"
      >
        <template #assignment>
          <IssueAssignment
            :assignee-id="localIssue.assignee?.id"
            :auth-user-id="authUserId"
            :status="localIssue.status"
            :is-editing="isEditing"
            @assign-to-me="assignToMe"
          />
        </template>
      </IssueDetails>

      <v-divider class="my-6"></v-divider>

      <CommentSection
        :comments="localIssue.comments"
        :auth-user-id="authUserId"
        :is-editing="isEditing"
        v-model="localComment"
        @submit-comment="submitComment"
        @delete-comment="handleDeleteComment"
        @update-comment="handleUpdateComment"
      />
    </v-card-text>

    <CommonSnackbar
      v-model="snackbarStore.isVisible"
      :message="snackbarStore.message"
      :timeout="snackbarStore.timeout"
      :color="snackbarStore.color"
    />
  </v-card>
  <SpinnerLoader v-else />
</template>

<script setup lang="ts">
import { defineProps, ref, onMounted } from 'vue';
import { useCommentsStore } from '@/stores/commentStore';
import { useAuthStore } from '@/stores/authStore';
import { useIssuesStore } from '@/stores/issueStore';
import { useSnackbarStore } from '@/stores/snackbarStore';
import type { Issue, NewComment, UpdateComment } from '@/types';
import IssueHeader from '@/components/issue/IssueHeader.vue';
import IssueDetails from '@/components/issue/IssueDetails.vue';
import IssueActions from '@/components/issue/IssueActions.vue';
import CommentSection from '@/components/comment/CommentSection.vue';
import CommonSnackbar from '@/components/common/CommonSnackbar.vue';
import SpinnerLoader from '@/components/common/SpinnerLoader.vue';
import IssueDates from './IssueDates.vue';
import IssueAssignment from './IssueAssignement.vue';

const commentsStore = useCommentsStore();
const issueStore = useIssuesStore();
const authStore = useAuthStore();
const snackbarStore = useSnackbarStore();

const props = defineProps<{ issueId: number }>();

const localIssue = ref<Issue | null>(null);
const authUserId = ref(authStore.user?.id);
const isEditing = ref(false);
const editedIssue = ref<Partial<Issue>>({});
const localComment = ref('');

onMounted(async () => await loadIssue());

const loadIssue = async () => {
  try {
    const issue = await issueStore.fetchIssue(props.issueId);
    localIssue.value = issue;
  } catch (err) {
    console.error('Ошибка при загрузке задачи:', err);
  }
};

const startEditing = () => {
  editedIssue.value = { ...localIssue.value };
  isEditing.value = true;
};

const saveChanges = async () => {
  if (!localIssue.value) return;
  const updateData = {
    title: editedIssue.value.title,
    description: editedIssue.value.description,
    status: editedIssue.value.status,
    priority: editedIssue.value.priority,
  };
  try {
    const updatedIssue = await issueStore.updateIssue(
      localIssue.value.id,
      updateData,
    );
    localIssue.value = updatedIssue;
    isEditing.value = false;
    snackbarStore.show('Задача успешно обновлена!', {
      color: 'success',
      timeout: 2000,
    });
  } catch (err) {
    console.error('Ошибка при сохранении изменений:', err);
    snackbarStore.show('Ошибка при сохранении изменений.', {
      color: 'error',
      timeout: 3000,
    });
  }
};

const cancelEditing = () => {
  isEditing.value = false;
  editedIssue.value = {};
};

const submitComment = async (content: string) => {
  if (!content.trim() || !localIssue.value) return;
  const newComment: NewComment = { content, issueId: localIssue.value.id };
  try {
    await commentsStore.createComment(newComment);
    localIssue.value.comments = await commentsStore.getCommentsByIssueId(
      localIssue.value.id,
    );

    localComment.value = '';

    snackbarStore.show('Комментарий успешно добавлен!', {
      color: 'success',
      timeout: 2000,
    });
  } catch (err) {
    console.error(err);

    snackbarStore.show('Ошибка при добавлении комментария.', {
      color: 'error',
      timeout: 3000,
    });
  }
};

const handleUpdateComment = async (id: number, comment: UpdateComment) => {
  try {
    await commentsStore.updateComment(id, comment);
    const updatedComment = await commentsStore.getCommentById(id);
    const index = localIssue.value!.comments.findIndex((c) => c.id === id);
    if (index !== -1) localIssue.value!.comments[index] = updatedComment;

    snackbarStore.show('Комментарий успешно изменен!', {
      color: 'success',
      timeout: 2000,
    });
  } catch (err) {
    console.error(err);

    snackbarStore.show('Ошибка при изменении комментария.', {
      color: 'error',
      timeout: 3000,
    });
  }
};

const handleDeleteComment = async (commentId: number) => {
  try {
    await commentsStore.deleteComment(commentId);
    localIssue.value!.comments = localIssue.value!.comments.filter(
      (c) => c.id !== commentId,
    );

    snackbarStore.show('Комментарий успешно удален!', {
      color: 'success',
      timeout: 2000,
    });
  } catch (err) {
    console.error(err);

    snackbarStore.show('Ошибка при удалении комментария.', {
      color: 'error',
      timeout: 3000,
    });
  }
};

const assignToMe = async () => {
  if (!localIssue.value) return;
  try {
    const updatedIssue = await issueStore.assignIssue(localIssue.value.id);
    localIssue.value = updatedIssue;

    snackbarStore.show('Задача успешно принята в работу!', {
      color: 'success',
      timeout: 2000,
    });
  } catch (err) {
    console.error('Ошибка при назначении задачи:', err);

    snackbarStore.show('Ошибка при назначении задачи.', {
      color: 'error',
      timeout: 3000,
    });
  }
};
</script>
