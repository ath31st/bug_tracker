import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Issue, NewIssue, UpdateIssue } from '@/types';
import * as issueApi from '@/api/issueApi';

export const useIssuesStore = defineStore('issues', () => {
  const issues = ref<Issue[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const getIssueById = computed(() => {
    return (issueId: number) =>
      issues.value.find((issue) => issue.id === issueId);
  });

  const issuesCount = computed(() => issues.value.length);

  async function fetchIssues() {
    try {
      loading.value = true;
      error.value = null;
      const response = await issueApi.getIssues();
      issues.value = response;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to fetch issues';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchIssue(id: number) {
    try {
      loading.value = true;
      error.value = null;
      const issue = await issueApi.getIssueById(id);
      const index = issues.value.findIndex((i) => i.id === id);
      if (index !== -1) {
        issues.value[index] = issue;
      } else {
        issues.value.push(issue);
      }
      return issue;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to fetch issue';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createIssue(issueData: NewIssue) {
    try {
      loading.value = true;
      error.value = null;
      const newIssue = await issueApi.createIssue(issueData);
      issues.value.push(newIssue);
      return newIssue;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to create issue';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateIssue(id: number, issueData: UpdateIssue) {
    try {
      loading.value = true;
      error.value = null;
      const updatedIssue = await issueApi.updateIssue(id, issueData);
      const index = issues.value.findIndex((i) => i.id === id);
      if (index !== -1) {
        issues.value[index] = updatedIssue;
      }
      return updatedIssue;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to update issue';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteIssue(id: number) {
    try {
      loading.value = true;
      error.value = null;
      await issueApi.deleteIssue(id);
      issues.value = issues.value.filter((issue) => issue.id !== id);
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to delete issue';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    issues,
    loading,
    error,

    getIssueById,
    issuesCount,

    fetchIssues,
    fetchIssue,
    createIssue,
    updateIssue,
    deleteIssue,
  };
});
