<template>
  <v-row>
    <v-col cols="7">
      <p>
        <strong v-if="!isEditing || authUserId !== reporterId"
          >Описание:</strong
        >
      </p>
      <p v-if="!isEditing || authUserId !== reporterId">
        {{ description }}
      </p>
      <v-textarea
        v-if="isEditing && authUserId === reporterId"
        v-model="localDescription"
        label="Описание"
        variant="outlined"
        hide-details="auto"
        @input="$emit('update:description', localDescription)"
      ></v-textarea>
    </v-col>

    <v-divider vertical></v-divider>

    <v-col cols="5">
      <v-row>
        <v-col cols="6"> <strong>Автор:</strong> {{ reporterUsername }} </v-col>
        <v-col cols="6">
          <strong v-if="!isEditing">Статус:</strong>
          <v-chip
            v-if="!isEditing"
            :color="getStatusColor(status)"
            class="ml-2"
          >
            {{ getStatusName(status) }}
          </v-chip>
          <v-select
            v-else
            v-model="localStatus"
            :items="statusOrder"
            :item-title="getStatusName"
            :item-value="(self) => self"
            label="Статус"
            variant="outlined"
            density="compact"
            hide-details="auto"
            @update:modelValue="$emit('update:status', localStatus)"
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <strong>Исполнитель:</strong>
          {{ assigneeUsername || 'Не назначен' }}
        </v-col>
        <v-col cols="6">
          <strong v-if="!isEditing">Приоритет:</strong>
          <v-chip
            v-if="!isEditing"
            :color="getPriorityColor(priority)"
            class="ml-2"
          >
            {{ getPriorityName(priority) }}
          </v-chip>
          <v-select
            v-if="isEditing && authUserId === reporterId"
            v-model="localPriority"
            :items="priorityOrder"
            :item-title="getPriorityName"
            :item-value="(self) => self"
            label="Приоритет"
            variant="outlined"
            density="compact"
            hide-details="auto"
            @update:modelValue="$emit('update:priority', localPriority)"
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <slot name="assignment"></slot>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
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
import { IssueStatus, Priority } from '@/types';

const props = defineProps<{
  description: string;
  status: IssueStatus;
  priority: Priority;
  reporterUsername: string;
  assigneeUsername?: string;
  reporterId: number | undefined;
  authUserId: number | undefined;
  isEditing: boolean;
}>();

defineEmits<{
  (e: 'update:description', value: string): void;
  (e: 'update:status', value: IssueStatus): void;
  (e: 'update:priority', value: Priority): void;
}>();

const localDescription = ref('');
const localStatus = ref(IssueStatus.NEW);
const localPriority = ref(Priority.MEDIUM);

watch(
  () => props.description,
  (newDesc) => (localDescription.value = newDesc),
  { immediate: true },
);

watch(
  () => props.status,
  (newStatus) => (localStatus.value = newStatus),
  { immediate: true },
);

watch(
  () => props.priority,
  (newPriority) => (localPriority.value = newPriority),
  { immediate: true },
);
</script>
