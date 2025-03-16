import type { Issue, NewIssue, Page, UpdateIssue } from '@/types';
import customAxios from '@/config/axiosConfig';

const ISSUES_PREFIX = '/issues/';

export const getIssues = async (
  page: number,
  elementsPerPage: number,
): Promise<Page<Issue>> => {
  const response = await customAxios.get(ISSUES_PREFIX, {
    params: {
      page: page,
      elementsPerPage: elementsPerPage,
    },
  });
  return response.data;
};

export const getIssueById = async (issueId: number): Promise<Issue> => {
  const response = await customAxios.get(`${ISSUES_PREFIX}${issueId}`);
  return response.data;
};

export const createIssue = async (issue: NewIssue): Promise<Issue> => {
  const response = await customAxios.post(ISSUES_PREFIX, issue);
  return response.data;
};

export const updateIssue = async (
  issueId: number,
  issue: UpdateIssue,
): Promise<Issue> => {
  const response = await customAxios.put(`${ISSUES_PREFIX}${issueId}`, issue);
  return response.data;
};

export const deleteIssue = async (issueId: number): Promise<void> => {
  await customAxios.delete(`${ISSUES_PREFIX}${issueId}`);
};

export const assignIssue = async (issueId: number): Promise<void> => {
  await customAxios.patch(`${ISSUES_PREFIX}${issueId}/assign`);
};
