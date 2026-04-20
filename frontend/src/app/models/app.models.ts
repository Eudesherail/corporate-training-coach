export interface User {
  id: number;
  full_name: string;
  email: string;
  role: 'admin' | 'employee';
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface DocumentItem {
  id: number;
  title: string;
  category: string;
  description: string;
  filename: string;
  uploaded_at: string;
  total_pages: number;
}

export interface Citation {
  document_name: string;
  page_number: number;
  excerpt: string;
}

export interface AssistantResponse {
  title: string;
  answer: string;
  citations: Citation[];
  mode: string;
}

export interface QuizQuestion {
  id: number;
  prompt: string;
  explanation: string;
  source_document: string;
  source_page: number;
}

export interface Quiz {
  id: number;
  title: string;
  document_id: number;
  questions: QuizQuestion[];
}

export interface ProgressRecord {
  id: number;
  module_name: string;
  status: string;
  completion_percent: number;
  notes: string;
  updated_at: string;
}
