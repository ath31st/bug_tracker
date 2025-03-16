import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { NewUser, UpdateUser } from '@/types';
import * as userApi from '@/api/userApi';

export const useUsersStore = defineStore('users', () => {
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function createUser(user: NewUser) {
    try {
      loading.value = true;
      error.value = null;
      await userApi.createUser(user);
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to create user';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateUser(id: number, userData: UpdateUser) {
    try {
      loading.value = true;
      error.value = null;
      const updatedUser = await userApi.updateUser(id, userData);
      return updatedUser;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to update user';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteUser(userId: number) {
    try {
      loading.value = true;
      error.value = null;
      await userApi.deleteUser(userId);
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to delete user';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    loading,
    error,

    createUser,
    updateUser,
    deleteUser,
  };
});
