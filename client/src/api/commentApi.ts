import type { Comment, NewComment, UpdateComment } from '@/types';
import axios from 'axios';

const API_URL = import.meta.env.PUBLIC_API_URL + '/comments';

export const getComments = async (issueId: number): Promise<Comment[]> => {
  const response = await axios.get(`${API_URL}/${issueId}`);
  return response.data;
};

export const getCommentById = async (commentId: number): Promise<Comment> => {
  const response = await axios.get(`${API_URL}/${commentId}`);
  return response.data;
};

export const createComment = async (comment: NewComment): Promise<Comment> => {
  const response = await axios.post(API_URL, comment);
  return response.data;
};

export const updateComment = async (
  commentId: number,
  comment: UpdateComment,
): Promise<Comment> => {
  const response = await axios.put(`${API_URL}/${commentId}`, comment);
  return response.data;
};

export const deleteComment = async (commentId: number): Promise<void> => {
  await axios.delete(`${API_URL}/${commentId}`);
};
