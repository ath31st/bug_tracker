<template>
  <div>
    <CommentList
      v-if="!isEditing"
      :comments="comments"
      :auth-user-id="authUserId"
      @delete="$emit('delete-comment', $event)"
      @update="
        ($eventId, $eventComment) =>
          $emit('update-comment', $eventId, $eventComment)
      "
    />

    <v-row v-if="!isEditing" class="mt-2 mb-2" align="center">
      <v-col cols="10">
        <v-text-field
          v-model="localComment"
          label="Добавить комментарий"
          variant="outlined"
          clearable
          density="compact"
          hide-details="auto"
          @keyup.enter="$emit('submit-comment', localComment)"
        ></v-text-field>
      </v-col>
      <v-col cols="2">
        <CommonButton
          class="w-100"
          variant="outlined"
          color="white"
          :disabled="!localComment || localComment.trim() === ''"
          @click="$emit('submit-comment', localComment)"
        >
          Отправить
        </CommonButton>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import CommentList from '@/components/comment/CommentList.vue';
import CommonButton from '@/components/common/CommonButton.vue';
import type { Comment, UpdateComment } from '@/types';

const props = defineProps<{
  comments: Comment[];
  authUserId: number | undefined;
  isEditing: boolean;
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: 'submit-comment', comment: string): void;
  (e: 'delete-comment', commentId: number): void;
  (e: 'update-comment', commentId: number, comment: UpdateComment): void;
  (e: 'update:modelValue', value: string): void;
}>();

const localComment = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit('update:modelValue', value);
  },
});
</script>
