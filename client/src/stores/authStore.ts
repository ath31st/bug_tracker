import type { Credentials } from '@/types';
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { login } from '@/api/authApi';
import { decodeToken } from '@/api/jwtApi';
import type { JwtUser } from '@/types';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null);
  const user = ref<JwtUser | null>(null);

  async function loginUser(credentials: Credentials) {
    try {
      const response = await login(credentials);

      if (response && response.accessToken) {
        const accessToken = response.accessToken;
        localStorage.setItem('token', accessToken);
        token.value = accessToken;
        user.value = decodeToken(accessToken);
        return { token: token.value, user: user.value };
      }

      return { token: null, user: null };
    } catch (error) {
      console.error('Login failed:', error);
      return { token: null, user: null };
    }
  }

  async function logout() {
    localStorage.removeItem('token');
    token.value = null;
    user.value = null;
  }

  return {
    token,
    user,
    loginUser,
  };
});
