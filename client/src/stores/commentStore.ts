import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Comment, NewComment, UpdateComment } from '@/types';
import * as commentApi from '@/api/commentApi';

export const useCommentsStore = defineStore('comments', () => {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const createComment = async (comment: NewComment): Promise<Comment> => {
    try {
      loading.value = true;
      error.value = null;
      const newComment = await commentApi.createComment(comment);
      return newComment;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to create comment';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getCommentsByIssueId = async (issueId: number): Promise<Comment[]> => {
    try {
      loading.value = true;
      error.value = null;
      const comments = await commentApi.getCommentsByIssueId(issueId);
      return comments;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to fetch comments';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateComment = async (commentId: number, comment: UpdateComment) => {
    try {
      loading.value = true;
      error.value = null;
      const updatedComment = await commentApi.updateComment(commentId, comment);
      return updatedComment;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to update comment';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deleteComment = async (commentId: number) => {
    try {
      loading.value = true;
      error.value = null;
      await commentApi.deleteComment(commentId);
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to delete comment';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    createComment,
    getCommentsByIssueId,
    updateComment,
    deleteComment,
  };
});
