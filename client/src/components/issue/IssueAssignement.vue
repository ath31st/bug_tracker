<template>
  <CommonButton
    v-if="!assigneeId && authUserId && !isEditing"
    variant="outlined"
    :disabled="status === 'CLOSED' || status === 'RESOLVED'"
    color="white"
    class="w-100"
    @click="$emit('assign-to-me')"
  >
    Взять в работу
  </CommonButton>
</template>

<script setup lang="ts">
import CommonButton from '@/components/common/CommonButton.vue';

defineProps<{
  authUserId: number | undefined;
  assigneeId?: number;
  isEditing: boolean;
  status: string;
}>();

defineEmits<{
  (e: 'assign-to-me'): void;
}>();
</script>
