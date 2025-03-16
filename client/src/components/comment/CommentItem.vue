<template>
  <v-list-item>
    <v-list-item-title>
      <strong>{{ comment.author.username }}</strong>
      <span class="comment-date">{{ formatDate(comment.createdAt) }}</span>
      <span
        v-if="
          !isEqualCreateAndUpdateDates(comment.createdAt, comment.updatedAt)
        "
        class="comment-date"
      >
        Изменен: {{ formatDate(comment.updatedAt) }}
      </span>
    </v-list-item-title>

    <template v-if="isEditing">
      <v-row align="center" class="mt-2">
        <v-col cols="10">
          <v-text-field
            v-model="editedContent"
            variant="outlined"
            clearable
            density="compact"
            hide-details="auto"
          ></v-text-field>
        </v-col>
        <v-col cols="2" class="d-flex justify-end">
          <v-btn variant="text" color="primary" @click="saveEdit">
            <v-icon>mdi-check</v-icon>
          </v-btn>
          <v-btn variant="text" color="error" @click="cancelEdit">
            <v-icon>mdi-cancel</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </template>
    <template v-else>
      <v-list-item-subtitle>{{ comment.content }}</v-list-item-subtitle>
    </template>

    <template v-if="isAuthor && !isEditing" #append>
      <v-btn variant="text" color="primary" @click="startEditing">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn variant="text" color="error" @click="isConfirmDialogOpen = true">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </template>

    <ConfirmDialog
      v-model="isConfirmDialogOpen"
      title="Удаление комментария"
      message="Вы уверены, что хотите удалить этот комментарий?"
      confirm-text="Удалить"
      cancel-text="Отмена"
      confirm-color="primary"
      cancel-color="error"
      @confirm="confirmDelete"
    />
  </v-list-item>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';
import { formatDate, isEqualCreateAndUpdateDates } from '@/utils/dateUtils';
import type { Comment, UpdateComment } from '@/types';
import ConfirmDialog from '@/components/modal/ConfirmDialog.vue';

const props = defineProps<{
  comment: Comment;
  isAuthor: boolean;
}>();

const emit = defineEmits<{
  (e: 'update', id: number, updatedComment: UpdateComment): void;
  (e: 'delete', id: number): void;
}>();

const isEditing = ref(false);
const editedContent = ref(props.comment.content);
const isConfirmDialogOpen = ref(false);

const startEditing = () => {
  editedContent.value = props.comment.content;
  isEditing.value = true;
};

const saveEdit = () => {
  if (!editedContent.value.trim()) return;

  const updatedComment: UpdateComment = {
    content: editedContent.value.trim(),
  };
  emit('update', props.comment.id, updatedComment);
  isEditing.value = false;
};

const cancelEdit = () => {
  isEditing.value = false;
  editedContent.value = props.comment.content;
};

const confirmDelete = () => {
  emit('delete', props.comment.id);
};
</script>

<style scoped>
.comment-date {
  font-size: 0.8rem;
  color: gray;
  margin-left: 8px;
}
</style>
