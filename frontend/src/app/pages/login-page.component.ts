import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login-page',
  template: `
    <section class="login-card">
      <div>
        <span class="eyebrow">Corporate Training Coach</span>
        <h2>Sign in to your onboarding workspace</h2>
        <p>
          Use the seeded demo accounts to explore the admin upload flow or the
          employee learning experience.
        </p>
      </div>

      <form (ngSubmit)="submit()">
        <label>
          Email
          <input [(ngModel)]="email" name="email" type="email" required />
        </label>

        <label>
          Password
          <input [(ngModel)]="password" name="password" type="password" required />
        </label>

        <button type="submit">Sign in</button>
      </form>

      <div class="demo-accounts">
        <strong>Demo accounts</strong>
        <p><code>admin@coach.com / Admin123!</code></p>
        <p><code>employee@coach.com / Employee123!</code></p>
      </div>

      <p class="error" *ngIf="error">{{ error }}</p>
    </section>
  `,
  styles: [`
    .login-card {
      max-width: 720px;
      margin: 4rem auto;
      padding: 2rem;
      border-radius: 24px;
      background: white;
      box-shadow: 0 20px 80px rgba(15, 23, 42, 0.12);
      display: grid;
      gap: 1.25rem;
    }
    .eyebrow {
      display: inline-block;
      color: #2563eb;
      font-weight: 700;
      margin-bottom: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 0.78rem;
    }
    form {
      display: grid;
      gap: 1rem;
    }
    label {
      display: grid;
      gap: 0.4rem;
      font-weight: 600;
    }
    input {
      padding: 0.9rem 1rem;
      border-radius: 14px;
      border: 1px solid #cbd5e1;
    }
    button {
      width: fit-content;
      padding: 0.9rem 1.3rem;
      border-radius: 999px;
      border: none;
      background: #0f172a;
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
    .demo-accounts {
      padding: 1rem;
      background: #eff6ff;
      border-radius: 16px;
    }
    .error {
      color: #b91c1c;
      font-weight: 600;
    }
  `]
})
export class LoginPageComponent {
  email = 'admin@coach.com';
  password = 'Admin123!';
  error = '';

  constructor(private authService: AuthService, private router: Router) {}

  submit(): void {
    this.error = '';
    this.authService.login(this.email, this.password).subscribe({
      next: (response) => {
        this.router.navigate([response.user.role === 'admin' ? '/admin' : '/employee']);
      },
      error: () => {
        this.error = 'Sign-in failed. Use one of the seeded demo accounts.';
      },
    });
  }
}
