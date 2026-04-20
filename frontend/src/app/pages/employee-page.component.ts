import { Component, OnInit } from '@angular/core';

import { ApiService } from '../services/api.service';
import { ProgressRecord, Quiz } from '../models/app.models';

@Component({
  selector: 'app-employee-page',
  template: `
    <section class="grid">
      <article class="panel">
        <h2>Employee dashboard</h2>
        <div class="metrics" *ngIf="dashboard">
          <div><strong>{{ dashboard.assigned_modules }}</strong><span>Assigned modules</span></div>
          <div><strong>{{ dashboard.completed_modules }}</strong><span>Completed modules</span></div>
          <div><strong>{{ dashboard.recent_quiz_average }}%</strong><span>Recent quiz average</span></div>
        </div>
      </article>

      <article class="panel">
        <h2>Your training progress</h2>
        <div *ngFor="let item of progress" class="progress-item">
          <strong>{{ item.module_name }}</strong>
          <p>{{ item.status }} · {{ item.completion_percent }}%</p>
          <small>{{ item.notes }}</small>
        </div>
      </article>

      <article class="panel full">
        <h2>Available quizzes</h2>
        <div class="quiz-card" *ngFor="let quiz of quizzes">
          <div>
            <strong>{{ quiz.title }}</strong>
            <p>{{ quiz.questions.length }} questions generated from indexed company documents</p>
          </div>
          <button type="button" (click)="takeQuiz(quiz)">Open quiz</button>
        </div>
      </article>

      <article class="panel full" *ngIf="activeQuiz">
        <h2>{{ activeQuiz.title }}</h2>
        <div *ngFor="let question of activeQuiz.questions" class="question">
          <strong>{{ question.prompt }}</strong>
          <textarea [(ngModel)]="answers[question.id]" rows="3" placeholder="Type your answer"></textarea>
          <small>Source: {{ question.source_document }} · Page {{ question.source_page }}</small>
        </div>
        <button type="button" (click)="submitQuiz()">Submit quiz</button>
        <p *ngIf="quizResult">{{ quizResult }}</p>
      </article>
    </section>
  `,
  styles: [`
    .grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1.5rem;
    }
    .panel {
      padding: 1.4rem;
      background: white;
      border-radius: 22px;
      box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
    }
    .full { grid-column: 1 / -1; }
    .metrics {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
    }
    .metrics div, .progress-item, .quiz-card, .question {
      padding: 1rem;
      border-radius: 16px;
      background: #f8fafc;
      margin-top: 0.8rem;
    }
    textarea, button {
      width: 100%;
      margin-top: 0.7rem;
      padding: 0.9rem 1rem;
      border-radius: 14px;
      border: 1px solid #cbd5e1;
      font: inherit;
    }
    button {
      width: auto;
      border: none;
      background: #0f766e;
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
    .quiz-card {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }
    @media (max-width: 900px) {
      .grid { grid-template-columns: 1fr; }
    }
  `]
})
export class EmployeePageComponent implements OnInit {
  dashboard: any;
  progress: ProgressRecord[] = [];
  quizzes: Quiz[] = [];
  activeQuiz?: Quiz;
  answers: Record<number, string> = {};
  quizResult = '';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.reload();
  }

  reload(): void {
    this.api.employeeDashboard().subscribe((data) => (this.dashboard = data));
    this.api.progress().subscribe((data) => (this.progress = data));
    this.api.quizzes().subscribe((data) => (this.quizzes = data));
  }

  takeQuiz(quiz: Quiz): void {
    this.activeQuiz = quiz;
    this.answers = {};
    this.quizResult = '';
  }

  submitQuiz(): void {
    if (!this.activeQuiz) {
      return;
    }
    this.api.submitQuiz(this.activeQuiz.id, this.answers).subscribe((result) => {
      this.quizResult = `Score: ${result.score_percent}% (${result.correct_answers}/${result.total_questions})`;
      this.reload();
    });
  }
}
