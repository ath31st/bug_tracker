import type { Comment, NewComment, UpdateComment } from '@/types';
import customAxios from '@/config/axiosConfig';

const COMMENTS_PREFIX = '/comments/';

export const getCommentsByIssueId = async (
  issueId: number,
): Promise<Comment[]> => {
  const response = await customAxios.get(`${COMMENTS_PREFIX}issue/${issueId}`);
  return response.data;
};

export const getCommentById = async (commentId: number): Promise<Comment> => {
  const response = await customAxios.get(`${COMMENTS_PREFIX}${commentId}`);
  return response.data;
};

export const createComment = async (comment: NewComment): Promise<Comment> => {
  const response = await customAxios.post(COMMENTS_PREFIX, comment);
  return response.data;
};

export const updateComment = async (
  commentId: number,
  comment: UpdateComment,
): Promise<Comment> => {
  const response = await customAxios.put(
    `${COMMENTS_PREFIX}${commentId}`,
    comment,
  );
  return response.data;
};

export const deleteComment = async (commentId: number): Promise<void> => {
  await customAxios.delete(`${COMMENTS_PREFIX}${commentId}`);
};
