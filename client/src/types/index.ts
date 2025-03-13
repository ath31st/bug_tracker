// auth types

export interface Credentials {
  username: string;
  password: string;
}

export interface JwtResponse {
  accessToken: string;
}

export interface JwtUser {
  userId: number;
  username: string;
}

// user types

export interface User {
  id: number;
  username: string;
  email: string;
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
  assigneeId?: number;
}

// comment types

export interface Comment {
  id: number;
  content: string;
  issue: Issue;
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
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical',
}

export enum IssueStatus {
  NEW = 'new',
  IN_PROGRESS = 'in_progress',
  RESOLVED = 'resolved',
  CLOSED = 'closed',
}
