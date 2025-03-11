import { Credentials, JwtResponse } from '@/types';
import axios from 'axios';

const API_URL = process.env.PUBLIC_API_URL + '/auth';

export const login = async (credentials: Credentials): Promise<JwtResponse> => {
  const response = await axios.post(`${API_URL}/login`, credentials);
  return response.data;
};
