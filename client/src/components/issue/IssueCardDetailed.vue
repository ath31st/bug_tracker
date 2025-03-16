<template>
  <v-card v-if="localIssue" class="pa-2">
    <v-card-title class="headline">
      <v-row align="center">
        <v-col cols="10">
          <span v-if="!isEditing || authUserId !== localIssue.reporter.id"
            >ID: {{ localIssue.id }} - {{ localIssue.title }}</span
          >
          <v-text-field
            v-if="isEditing && authUserId === localIssue.reporter.id"
            class="mt-4"
            v-model="editedIssue.title"
            label="Заголовок"
            variant="outlined"
            density="compact"
            hide-details="auto"
          ></v-text-field>
        </v-col>
        <v-col cols="2" class="text-right">
          <v-btn
            v-if="
              (authUserId === localIssue.reporter.id ||
                authUserId === localIssue.assignee?.id) &&
              !isEditing
            "
            variant="text"
            color="primary"
            @click="startEditing"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>

          <v-btn
            v-if="isEditing"
            variant="text"
            color="primary"
            @click="saveChanges"
          >
            <v-icon>mdi-check</v-icon>
          </v-btn>

          <v-btn
            v-if="isEditing"
            variant="text"
            color="error"
            @click="cancelEditing"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-col>
      </v-row>
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
          <p>
            <strong v-if="!isEditing || authUserId !== localIssue.reporter.id"
              >Описание:</strong
            >
          </p>
          <p v-if="!isEditing || authUserId !== localIssue.reporter.id">
            {{ localIssue.description }}
          </p>
          <v-textarea
            v-if="isEditing && authUserId === localIssue.reporter.id"
            v-model="editedIssue.description"
            label="Описание"
            variant="outlined"
            hide-details="auto"
          ></v-textarea>
        </v-col>

        <v-divider vertical></v-divider>

        <v-col cols="5">
          <v-row>
            <v-col cols="6">
              <strong>Автор:</strong> {{ localIssue.reporter.username }}
            </v-col>
            <v-col cols="6">
              <strong v-if="!isEditing">Статус:</strong>
              <v-chip
                v-if="!isEditing"
                :color="getStatusColor(localIssue.status)"
                class="ml-2"
              >
                {{ getStatusName(localIssue.status) }}
              </v-chip>
              <v-select
                v-else
                v-model="editedIssue.status"
                :items="statusOrder"
                :item-title="getStatusName"
                :item-value="(self) => self"
                label="Статус"
                variant="outlined"
                density="compact"
                hide-details="auto"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <strong>Исполнитель:</strong>
              {{ localIssue.assignee?.username || 'Не назначен' }}
            </v-col>
            <v-col cols="6">
              <strong v-if="!isEditing">Приоритет:</strong>
              <v-chip
                v-if="!isEditing"
                :color="getPriorityColor(localIssue.priority)"
                class="ml-2"
              >
                {{ getPriorityName(localIssue.priority) }}
              </v-chip>
              <v-select
                v-if="isEditing && authUserId === localIssue.reporter.id"
                v-model="editedIssue.priority"
                :items="priorityOrder"
                :item-title="getPriorityName"
                :item-value="(self) => self"
                label="Приоритет"
                variant="outlined"
                density="compact"
                hide-details="auto"
              ></v-select>
            </v-col>
          </v-row>
          <v-row v-if="!localIssue.assignee && authUserId && !isEditing">
            <v-col cols="12" class="pt-2">
              <CommonButton
                variant="outlined"
                :disabled="
                  localIssue.status == IssueStatus.CLOSED ||
                  localIssue.status == IssueStatus.RESOLVED
                "
                color="white"
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
        v-if="!isEditing"
        :comments="localIssue.comments"
        :auth-user-id="authUserId"
        @delete="handleDeleteComment"
        @update="handleUpdateComment"
      />

      <v-row v-if="!isEditing" class="mt-2 mb-2" align="center">
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
import { formatDate, isEqualCreateAndUpdateDates } from '@/utils/dateUtils';
import {
  getStatusColor,
  getStatusName,
  statusOrder,
} from '@/utils/statusUtils';
import {
  getPriorityColor,
  getPriorityName,
  priorityOrder,
} from '@/utils/priorityUtils';
import {
  IssueStatus,
  type Issue,
  type NewComment,
  type UpdateComment,
  type UpdateIssue,
} from '@/types';
import CommentList from '@/components/comment/CommentList.vue';
import { useCommentsStore } from '@/stores/commentStore';
import { useAuthStore } from '@/stores/authStore';
import { useIssuesStore } from '@/stores/issueStore';
import CommonButton from '../button/CommonButton.vue';
import SpinnerLoader from '@/components/loader/SpinnerLoader.vue';
import { useSnackbarStore } from '@/stores/snackbarStore';
import CommonSnackbar from '../CommonSnackbar.vue';

const commentsStore = useCommentsStore();
const issueStore = useIssuesStore();
const authStore = useAuthStore();
const snackbarStore = useSnackbarStore();

const props = defineProps<{
  issueId: number;
}>();

const localIssue = ref<Issue | null>(null);
const authUserId = ref(authStore.user?.id);
const comment = ref('');
const isEditing = ref(false);
const editedIssue = ref<Partial<Issue>>({});

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
  } finally {
    comment.value = '';
  }
};

function startEditing() {
  editedIssue.value = { ...localIssue.value };
  isEditing.value = true;
}

async function saveChanges() {
  if (!localIssue.value) return;

  const updateData: UpdateIssue = {
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
}

function cancelEditing() {
  isEditing.value = false;
  editedIssue.value = {};
}

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

<style scoped>
.headline {
  font-size: 1.5rem;
  font-weight: bold;
}

.v-card-subtitle {
  margin-top: 8px;
}
</style>
