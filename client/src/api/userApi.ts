import type { NewUser, UpdateUser, User } from '@/types';
import axios from 'axios';

const API_URL = import.meta.env.PUBLIC_API_URL + '/users';

export const getUsers = async (): Promise<User[]> => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const getUser = async (userId: number): Promise<User> => {
  const response = await axios.get(`${API_URL}/${userId}`);
  return response.data;
};

export const createUser = async (user: NewUser): Promise<User> => {
  const response = await axios.post(API_URL, user);
  return response.data;
};

export const updateUser = async (
  userId: number,
  user: UpdateUser,
): Promise<User> => {
  const response = await axios.put(`${API_URL}/${userId}`, user);
  return response.data;
};

export const deleteUser = async (userId: number): Promise<void> => {
  await axios.delete(`${API_URL}/${userId}`);
};
