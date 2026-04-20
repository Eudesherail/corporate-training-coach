import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';

import { environment } from '../../environments/environment';
import { LoginResponse, User } from '../models/app.models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly apiUrl = `${environment.backendUrl}/api`;

  constructor(private http: HttpClient, private router: Router) {}

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${this.apiUrl}/auth/login`, { email, password })
      .pipe(
        tap((response) => {
          localStorage.setItem('ctc_token', response.access_token);
          localStorage.setItem('ctc_user', JSON.stringify(response.user));
        })
      );
  }

  logout(): void {
    localStorage.removeItem('ctc_token');
    localStorage.removeItem('ctc_user');
    this.router.navigate(['/login']);
  }

  token(): string | null {
    return localStorage.getItem('ctc_token');
  }

  currentUser(): User | null {
    const raw = localStorage.getItem('ctc_user');
    return raw ? JSON.parse(raw) : null;
  }

  isAuthenticated(): boolean {
    return !!this.token();
  }

  isAdmin(): boolean {
    return this.currentUser()?.role === 'admin';
  }
}
