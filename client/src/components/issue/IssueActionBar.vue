<template>
  <v-card-actions>
    <v-row justify="start">
      <v-col cols="2">
        <CommonButton class="w-100" variant="outlined" to="/new-issue">
          <v-icon>mdi-bug</v-icon>
          Создать заявку
        </CommonButton>
      </v-col>
      <v-col cols="2">
        <CommonButton
          class="w-100"
          :variant="isMyIssuesActive ? 'elevated' : 'outlined'"
          @click="$emit('toggle-my-issues')"
        >
          <v-icon>mdi-account</v-icon>
          Мои заявки
        </CommonButton>
      </v-col>
      <v-col cols="2">
        <CommonButton
          class="w-100"
          :variant="isAssignedToMeActive ? 'elevated' : 'outlined'"
          @click="$emit('toggle-assigned-to-me')"
        >
          <v-icon>mdi-account-check</v-icon>
          Приняты в работу
        </CommonButton>
      </v-col>
    </v-row>
  </v-card-actions>
</template>

<script setup lang="ts">
import CommonButton from '@/components/common/CommonButton.vue';

defineProps<{
  isMyIssuesActive: boolean;
  isAssignedToMeActive: boolean;
}>();

defineEmits<{
  (e: 'toggle-my-issues'): void;
  (e: 'toggle-assigned-to-me'): void;
}>();
</script>
