<template>
  <v-card-actions>
    <v-row>
      <v-col>
        <CommonButton variant="outlined" to="/new-issue">
          <v-icon>mdi-bug</v-icon>
          Создать
        </CommonButton>
      </v-col>
    </v-row>
  </v-card-actions>
</template>

<script setup lang="ts">
import CommonButton from '@/components/button/CommonButton.vue';
</script>
