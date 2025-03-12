import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Issue, NewIssue, UpdateIssue } from '@/types';
import * as issueApi from '@/api/issueApi';

export const useIssuesStore = defineStore('issues', () => {
  const issues = ref<Issue[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const elementsPerPage = ref(10);
  const totalItems = ref(0);
  const totalPages = ref(0);

  const getIssueById = computed(() => {
    return (issueId: number) =>
      issues.value.find((issue) => issue.id === issueId);
  });

  const issuesCount = computed(() => issues.value.length);

  async function fetchIssues(page?: number, perPage?: number) {
    try {
      loading.value = true;
      error.value = null;

      const pageToFetch = page ?? currentPage.value;
      const perPageToFetch = perPage ?? elementsPerPage.value;

      const response = await issueApi.getIssues(pageToFetch, perPageToFetch);

      issues.value = response.items;
      currentPage.value = response.currentPage;
      totalItems.value = response.totalItems;
      totalPages.value = response.totalPages;
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
      totalItems.value += 1;
      totalPages.value = Math.ceil(totalItems.value / elementsPerPage.value);

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

      totalItems.value -= 1;
      totalPages.value = Math.ceil(totalItems.value / elementsPerPage.value);

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

  async function setPage(page: number) {
    if (page >= 1 && page <= totalPages.value) {
      await fetchIssues(page);
    }
  }

  async function setElementsPerPage(perPage: number) {
    if (perPage > 0) {
      await fetchIssues(1, perPage);
    }
  }

  return {
    issues,
    loading,
    error,
    currentPage,
    elementsPerPage,
    totalItems,
    totalPages,

    getIssueById,
    issuesCount,

    fetchIssues,
    fetchIssue,
    createIssue,
    updateIssue,
    deleteIssue,
    setPage,
    setElementsPerPage,
  };
});
