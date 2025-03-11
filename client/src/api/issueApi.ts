import type { Issue, NewIssue } from '@/types';
import axios from 'axios';

const API_URL = import.meta.env.PUBLIC_API_URL + '/issues';

export const getIssues = async (): Promise<Issue[]> => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const getIssueById = async (issueId: number): Promise<Issue> => {
  const response = await axios.get(`${API_URL}/${issueId}`);
  return response.data;
};

export const createIssue = async (issue: Issue): Promise<NewIssue> => {
  const response = await axios.post(API_URL, issue);
  return response.data;
};

export const updateIssue = async (
  issueId: number,
  issue: Issue,
): Promise<Issue> => {
  const response = await axios.put(`${API_URL}/${issueId}`, issue);
  return response.data;
};

export const deleteIssue = async (issueId: number): Promise<void> => {
  await axios.delete(`${API_URL}/${issueId}`);
};
