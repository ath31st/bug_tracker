<template>
  <div>
    <v-btn
      v-if="
        (authUserId === reporterId || authUserId === assigneeId) && !isEditing
      "
      variant="text"
      color="primary"
      @click="$emit('start-editing')"
    >
      <v-icon>mdi-pencil</v-icon>
    </v-btn>

    <v-btn
      v-if="isEditing"
      variant="text"
      color="primary"
      @click="$emit('save-changes')"
    >
      <v-icon>mdi-check</v-icon>
    </v-btn>

    <v-btn
      v-if="isEditing"
      variant="text"
      color="error"
      @click="$emit('cancel-editing')"
    >
      <v-icon>mdi-close</v-icon>
    </v-btn>

    <v-row v-if="!assigneeId && authUserId && !isEditing">
      <v-col cols="12" class="pt-2">
        <CommonButton
          variant="outlined"
          :disabled="status === 'CLOSED' || status === 'RESOLVED'"
          color="white"
          class="w-100"
          @click="$emit('assign-to-me')"
        >
          Взять в работу
        </CommonButton>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import CommonButton from '../common/CommonButton.vue';

defineProps<{
  authUserId: number | undefined;
  reporterId: number | undefined;
  assigneeId?: number;
  isEditing: boolean;
  status: string;
}>();

defineEmits<{
  (e: 'start-editing'): void;
  (e: 'save-changes'): void;
  (e: 'cancel-editing'): void;
  (e: 'assign-to-me'): void;
}>();
</script>
