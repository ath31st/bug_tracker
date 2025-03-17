<template>
  <div>
    <h1>Страница не найдена</h1>
    <p class="mt-6">К сожалению, такой страницы не существует.</p>
    <CommonButton class="mt-8" variant="outlined" to="/"
      >Вернуться на главную</CommonButton
    >
  </div>
</template>

<script setup lang="ts">
import CommonButton from '@/components/common/CommonButton.vue';
</script>

<style scoped>
div {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 70vh;
}
</style>
