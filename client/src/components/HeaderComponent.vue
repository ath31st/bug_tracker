<template>
  <v-app-bar app color="primary">
    <v-toolbar-title>
      <router-link to="/" class="text-decoration-none" style="color: inherit">
        <h3>Bug tracker</h3>
      </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>

    <div class="d-flex">
      <v-btn text to="/" exact>Главная</v-btn>
      <v-btn text to="/about">О проекте</v-btn>

      <template v-if="authStore.user">
        <v-btn text @click="logout">Выход</v-btn>
        <v-btn @click="openUserModal">
          {{ authStore.user?.username.toUpperCase() || 'User' }}
        </v-btn>
      </template>
    </div>
  </v-app-bar>

  <UserModal
    :user="selectedUser"
    :visible="isModalVisible"
    @close="closeUserModal"
  />
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore';
import { useUsersStore } from '@/stores/userStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import UserModal from '@/components/user/UserModal.vue';
import type { User } from '@/types';

const authStore = useAuthStore();
const usersStore = useUsersStore();
const router = useRouter();

const isModalVisible = ref(false);
const selectedUser = ref<User | null>(null);

function logout() {
  authStore.logout();
  router.push('/login');
}

const fetchUser = async (userId: number) => {
  try {
    const user = await usersStore.fetchUser(userId);
    return user;
  } catch (error) {
    console.error('Ошибка при загрузке пользователя:', error);
    return null;
  }
};

const openUserModal = async () => {
  if (authStore.user?.id) {
    const user = await fetchUser(authStore.user.id);
    if (user) {
      selectedUser.value = user;
      isModalVisible.value = true;
    }
  }
};

const closeUserModal = () => {
  isModalVisible.value = false;
  selectedUser.value = null;
};
</script>

<style scoped>
.d-flex > * {
  margin-right: 16px;
}
.v-btn {
  width: 100px;
}
</style>
