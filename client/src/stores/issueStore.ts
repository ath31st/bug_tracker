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
  const sortKey = ref<string>('createdAt');
  const sortDirection = ref<'asc' | 'desc'>('asc');
  const filterReporterId = ref<number | undefined>(undefined);
  const filterAssigneeId = ref<number | undefined>(undefined);

  const getIssueById = computed(() => {
    return (issueId: number) =>
      issues.value.find((issue) => issue.id === issueId);
  });

  const issuesCount = computed(() => issues.value.length);

  async function fetchIssues(
    key?: string,
    direction?: 'asc' | 'desc',
    page?: number,
    perPage?: number,
    reporterId?: number,
    assigneeId?: number,
  ) {
    try {
      loading.value = true;
      error.value = null;

      const pageToFetch = page ?? currentPage.value;
      const perPageToFetch = perPage ?? elementsPerPage.value;
      const sortKeyToFetch = key ?? sortKey.value;
      const sortDirectionToFetch = direction ?? sortDirection.value;
      const reporterIdToFetch = reporterId ?? filterReporterId.value;
      const assigneeIdToFetch = assigneeId ?? filterAssigneeId.value;

      const response = await issueApi.getIssues(
        pageToFetch,
        perPageToFetch,
        sortKeyToFetch,
        sortDirectionToFetch,
        reporterIdToFetch,
        assigneeIdToFetch,
      );

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

  async function assignIssue(issueId: number): Promise<Issue> {
    try {
      loading.value = true;
      error.value = null;
      const updatedIssue = await issueApi.assignIssue(issueId);
      const index = issues.value.findIndex((i) => i.id === issueId);
      if (index !== -1) {
        issues.value[index] = updatedIssue;
      } else {
        issues.value.push(updatedIssue);
      }
      return updatedIssue;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Failed to assign issue';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function setPage(page: number) {
    if (page >= 1 && page <= totalPages.value) {
      await fetchIssues(sortKey.value, sortDirection.value, page);
    }
  }

  async function setElementsPerPage(perPage: number) {
    if (perPage > 0) {
      await fetchIssues(sortKey.value, sortDirection.value, 1, perPage);
    }
  }

  const setSort = async (key: string, direction: 'asc' | 'desc') => {
    sortKey.value = key;
    sortDirection.value = direction;
  };

  const setFilters = async (
    reporterId: number | undefined,
    assigneeId: number | undefined,
  ) => {
    filterReporterId.value = reporterId;
    filterAssigneeId.value = assigneeId;
  };

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
    assignIssue,
    setPage,
    setElementsPerPage,
    setSort,
    setFilters,
  };
});
