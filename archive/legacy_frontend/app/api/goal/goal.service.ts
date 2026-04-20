// src/app/goal.service.ts
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class GoalService {
  //private apiUrl = 'https://stubu-app-paddy-90.cloud.okteto.net/api/users';
  private apiUrl = `${environment.backendUrl}/api`;
  constructor(private http: HttpClient) {}

  private createHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  getGoals(userId: number): Observable<any> {
    const headers = this.createHeaders();
    return this.http.get<any>(`${this.apiUrl}/goals/`, { headers: headers });
  }

  getGoal(userId: number, goalId: number): Observable<any> {
    const headers = this.createHeaders();
    return this.http.get<any>(`${this.apiUrl}/${userId}/goals/${goalId}/`, { headers: headers });
  }

  updateGoal(userId: number, goalId: number, goalData: any): Observable<any> {
    const headers = this.createHeaders();
    return this.http.put<any>(`${this.apiUrl}/goals/${goalId}/`, goalData, { headers: headers });
  }

  deleteGoal(userId: number, goalId: number): Observable<any> {
    const headers = this.createHeaders();
    return this.http.delete<any>(`${this.apiUrl}/goals/${goalId}/`, { headers: headers });
  }

  createGoal(userId: number, goalData: any): Observable<any> {
    const headers = this.createHeaders();
    return this.http.post<any>(`${this.apiUrl}/goals/`, goalData, { headers: headers });
  }
}
