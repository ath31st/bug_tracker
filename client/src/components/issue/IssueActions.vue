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
  </div>
</template>

<script setup lang="ts">
defineProps<{
  authUserId: number | undefined;
  reporterId: number | undefined;
  assigneeId?: number;
  isEditing: boolean;
}>();

defineEmits<{
  (e: 'start-editing'): void;
  (e: 'save-changes'): void;
  (e: 'cancel-editing'): void;
}>();
</script>
