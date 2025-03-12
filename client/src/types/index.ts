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
  status: string;
  priority: string;
  reporter: User;
  assignee?: User;
  comments: Comment[];
  created_at: string;
  updated_at: string;
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
  assignee_id?: number;
}

// comment types

export interface Comment {
  id: number;
  content: string;
  issue: Issue;
  created_at: string;
  updated_at: string;
  author: User;
}

export interface NewComment {
  content: string;
  issue_id: number;
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
