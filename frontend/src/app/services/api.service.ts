import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import {
  AssistantResponse,
  DocumentItem,
  ProgressRecord,
  Quiz,
} from '../models/app.models';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly apiUrl = `${environment.backendUrl}/api`;

  constructor(private http: HttpClient, private authService: AuthService) {}

  private headers(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `Bearer ${this.authService.token() ?? ''}`,
    });
  }

  documents(): Observable<DocumentItem[]> {
    return this.http.get<DocumentItem[]>(`${this.apiUrl}/documents`, {
      headers: this.headers(),
    });
  }

  uploadDocument(formData: FormData): Observable<DocumentItem> {
    return this.http.post<DocumentItem>(`${this.apiUrl}/documents/upload`, formData, {
      headers: this.headers(),
    });
  }

  askAssistant(question: string): Observable<AssistantResponse> {
    return this.http.post<AssistantResponse>(
      `${this.apiUrl}/assistant/ask`,
      { question },
      { headers: this.headers() }
    );
  }

  generateQuiz(documentId: number, title: string): Observable<Quiz> {
    return this.http.post<Quiz>(
      `${this.apiUrl}/quizzes/generate`,
      { document_id: documentId, title, question_count: 5 },
      { headers: this.headers() }
    );
  }

  quizzes(): Observable<Quiz[]> {
    return this.http.get<Quiz[]>(`${this.apiUrl}/quizzes`, {
      headers: this.headers(),
    });
  }

  submitQuiz(quizId: number, answers: Record<number, string>) {
    return this.http.post<{ score_percent: number; total_questions: number; correct_answers: number }>(
      `${this.apiUrl}/quizzes/${quizId}/submit`,
      { answers },
      { headers: this.headers() }
    );
  }

  progress(): Observable<ProgressRecord[]> {
    return this.http.get<ProgressRecord[]>(`${this.apiUrl}/progress/me`, {
      headers: this.headers(),
    });
  }

  updateProgress(payload: {
    module_name: string;
    document_id?: number;
    status: string;
    completion_percent: number;
    notes: string;
  }): Observable<ProgressRecord> {
    return this.http.post<ProgressRecord>(`${this.apiUrl}/progress`, payload, {
      headers: this.headers(),
    });
  }

  adminDashboard() {
    return this.http.get<{
      total_documents: number;
      total_quizzes: number;
      total_employees: number;
      active_progress_records: number;
    }>(`${this.apiUrl}/dashboard/admin`, { headers: this.headers() });
  }

  employeeDashboard() {
    return this.http.get<{
      assigned_modules: number;
      completed_modules: number;
      recent_quiz_average: number;
    }>(`${this.apiUrl}/dashboard/employee`, { headers: this.headers() });
  }

  users() {
    return this.http.get<any[]>(`${this.apiUrl}/users`, { headers: this.headers() });
  }
}
