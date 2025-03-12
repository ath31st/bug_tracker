import type { Issue, NewIssue, Page, UpdateIssue } from '@/types';
import axios from 'axios';

const API_URL = import.meta.env.VITE_PUBLIC_API_URL + '/issues';

export const getIssues = async (
  page: number,
  elementsPerPage: number,
): Promise<Page<Issue>> => {
  const response = await axios.get(API_URL, {
    params: {
      page: page,
      elementsPerPage: elementsPerPage,
    },
  });
  return response.data;
};

export const getIssueById = async (issueId: number): Promise<Issue> => {
  const response = await axios.get(`${API_URL}/${issueId}`);
  return response.data;
};

export const createIssue = async (issue: NewIssue): Promise<Issue> => {
  const response = await axios.post(API_URL, issue);
  return response.data;
};

export const updateIssue = async (
  issueId: number,
  issue: UpdateIssue,
): Promise<Issue> => {
  const response = await axios.put(`${API_URL}/${issueId}`, issue);
  return response.data;
};

export const deleteIssue = async (issueId: number): Promise<void> => {
  await axios.delete(`${API_URL}/${issueId}`);
};
