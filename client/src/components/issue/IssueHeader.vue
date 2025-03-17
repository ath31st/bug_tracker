<template>
  <v-row align="center">
    <v-col cols="10">
      <span v-if="!isEditing || authUserId !== reporterId"
        >ID: {{ issueId }} - {{ title }}</span
      >
      <v-text-field
        v-if="isEditing && authUserId === reporterId"
        class="mt-4"
        v-model="localTitle"
        label="Заголовок"
        variant="outlined"
        density="compact"
        hide-details="auto"
        @input="$emit('update:title', localTitle)"
      ></v-text-field>
    </v-col>
    <v-col cols="2" class="text-right">
      <slot name="actions"></slot>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  issueId: number;
  title: string;
  reporterId: number | undefined;
  authUserId: number | undefined;
  isEditing: boolean;
}>();

defineEmits<{
  (e: 'update:title', value: string): void;
}>();

const localTitle = ref('');

watch(
  () => props.title,
  (newTitle) => {
    localTitle.value = newTitle;
  },
  { immediate: true },
);
</script>
