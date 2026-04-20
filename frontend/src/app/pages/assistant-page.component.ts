import { Component } from '@angular/core';

import { AssistantResponse } from '../models/app.models';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-assistant-page',
  template: `
    <section class="assistant-layout">
      <article class="panel composer">
        <h2>Ask the training assistant</h2>
        <p>
          Ask grounded questions about onboarding, SOPs, compliance expectations,
          and internal policies. If no context is found, the assistant will say so.
        </p>
        <textarea [(ngModel)]="question" rows="5" placeholder="How do I request leave during onboarding?"></textarea>
        <button type="button" (click)="ask()">Retrieve answer</button>
      </article>

      <article class="panel answer" *ngIf="response">
        <h2>{{ response.title }}</h2>
        <pre>{{ response.answer }}</pre>
        <div *ngIf="response.citations.length">
          <h3>Sources</h3>
          <div class="citation" *ngFor="let citation of response.citations">
            <strong>{{ citation.document_name }} · Page {{ citation.page_number }}</strong>
            <p>{{ citation.excerpt }}</p>
          </div>
        </div>
        <p *ngIf="!response.citations.length">No relevant source found in provided documents.</p>
      </article>
    </section>
  `,
  styles: [`
    .assistant-layout {
      display: grid;
      grid-template-columns: minmax(320px, 460px) 1fr;
      gap: 1.5rem;
    }
    .panel {
      padding: 1.5rem;
      background: white;
      border-radius: 24px;
      box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
    }
    textarea, button {
      width: 100%;
      margin-top: 1rem;
      padding: 0.95rem 1rem;
      border-radius: 16px;
      border: 1px solid #cbd5e1;
      font: inherit;
    }
    button {
      border: none;
      background: #1d4ed8;
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
    pre {
      white-space: pre-wrap;
      font-family: inherit;
      line-height: 1.6;
      background: #f8fafc;
      padding: 1rem;
      border-radius: 16px;
    }
    .citation {
      margin-top: 0.8rem;
      padding: 1rem;
      border-radius: 16px;
      background: #eff6ff;
    }
    @media (max-width: 900px) {
      .assistant-layout {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class AssistantPageComponent {
  question = '';
  response?: AssistantResponse;

  constructor(private api: ApiService) {}

  ask(): void {
    if (!this.question.trim()) {
      return;
    }
    this.api.askAssistant(this.question).subscribe((data) => (this.response = data));
  }
}
