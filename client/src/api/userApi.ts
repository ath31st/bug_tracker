import type { NewUser, UpdateUser, User } from '@/types';
import customAxios from '@/config/axiosConfig';

const USERS_PREFIX = '/users/';

export const getUsers = async (): Promise<User[]> => {
  const response = await customAxios.get(USERS_PREFIX);
  return response.data;
};

export const getUser = async (userId: number): Promise<User> => {
  const response = await customAxios.get(`${USERS_PREFIX}${userId}`);
  return response.data;
};

export const createUser = async (user: NewUser): Promise<User> => {
  const response = await customAxios.post(USERS_PREFIX, user);
  return response.data;
};

export const updateUser = async (
  userId: number,
  user: UpdateUser,
): Promise<User> => {
  const response = await customAxios.put(`${USERS_PREFIX}${userId}`, user);
  return response.data;
};

export const deleteUser = async (userId: number): Promise<void> => {
  await customAxios.delete(`${USERS_PREFIX}${userId}`);
};
