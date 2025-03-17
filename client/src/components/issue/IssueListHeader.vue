<template>
  <v-row class="px-5 mt-2">
    <v-col cols="1" class="header-col clickable" @click="sort('id')">
      <span>ID</span>
      <v-icon v-if="sortKey === 'id'" size="small">
        {{ sortDirection === 'asc' ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
      </v-icon>
    </v-col>
    <v-col cols="2" class="header-col">
      <span>Заголовок</span>
    </v-col>
    <v-col cols="1" class="header-col clickable" @click="sort('status')">
      <span>Статус</span>
      <v-icon v-if="sortKey === 'status'" size="small">
        {{ sortDirection === 'asc' ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
      </v-icon>
    </v-col>
    <v-col cols="1" class="header-col clickable" @click="sort('priority')">
      <span>Приоритет</span>
      <v-icon v-if="sortKey === 'priority'" size="small">
        {{ sortDirection === 'asc' ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
      </v-icon>
    </v-col>
    <v-col cols="2" class="header-col">
      <span>Автор</span>
    </v-col>
    <v-col cols="2" class="header-col">
      <span>Исполнитель</span>
    </v-col>
    <v-col cols="3" class="header-col clickable" @click="sort('created_at')">
      <span>Дата создания</span>
      <v-icon v-if="sortKey === 'created_at'" size="small">
        {{ sortDirection === 'asc' ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
      </v-icon>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const sortKey = ref<string | null>(null);
const sortDirection = ref<'asc' | 'desc'>('asc');

const emit = defineEmits(['sort']);

const sort = (key: string) => {
  if (sortKey.value === key) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortDirection.value = 'asc';
  }
  emit('sort', { key: sortKey.value, direction: sortDirection.value });
};
</script>

<style scoped>
.header-col {
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
}

.clickable {
  cursor: pointer;
  user-select: none;
}
</style>
