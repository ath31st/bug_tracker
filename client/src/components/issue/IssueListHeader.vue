<template>
  <v-row class="px-5">
    <v-col cols="1" class="header-col">
      <span>ID</span>
    </v-col>
    <v-col cols="2" class="header-col">
      <span>Заголовок</span>
    </v-col>
    <v-col cols="1" class="header-col">
      <span>Статус</span>
    </v-col>
    <v-col cols="1" class="header-col">
      <span>Приоритет</span>
    </v-col>
    <v-col cols="2" class="header-col">
      <span>Автор</span>
    </v-col>
    <v-col cols="2" class="header-col">
      <span>Исполнитель</span>
    </v-col>
    <v-col cols="3" class="header-col">
      <span>Дата создания</span>
    </v-col>
  </v-row>
</template>

<script setup lang="ts"></script>

<style scoped>
.header-col {
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
}
</style>
