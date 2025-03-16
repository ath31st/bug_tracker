// auth types

export interface Credentials {
  username: string;
  password: string;
}

export interface JwtResponse {
  accessToken: string;
}

export interface JwtUser {
  id: number;
  username: string;
}

// user types

export interface User {
  id: number;
  username: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}

export interface NewUser {
  username: string;
  email: string;
  password: string;
}

export interface UpdateUser {
  username?: string;
  email?: string;
  password?: string;
}

// issue types

export interface Issue {
  id: number;
  title: string;
  description: string;
  status: IssueStatus;
  priority: Priority;
  reporter: User;
  assignee?: User;
  comments: Comment[];
  createdAt: string;
  updatedAt: string;
}

export interface NewIssue {
  title: string;
  description: string;
  priority: string;
}

export interface UpdateIssue {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
}

// comment types

export interface Comment {
  id: number;
  content: string;
  issueId: number;
  createdAt: string;
  updatedAt: string;
  author: User;
}

export interface NewComment {
  content: string;
  issueId: number;
}

export interface UpdateComment {
  content?: string;
}

// page types

export interface Page<T> {
  items: T[];
  totalItems: number;
  totalPages: number;
  currentPage: number;
}

// enums

export enum Priority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL',
}

export enum IssueStatus {
  NEW = 'NEW',
  IN_PROGRESS = 'IN_PROGRESS',
  RESOLVED = 'RESOLVED',
  CLOSED = 'CLOSED',
}
