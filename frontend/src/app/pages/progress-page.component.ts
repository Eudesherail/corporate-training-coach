import { Component, OnInit } from '@angular/core';

import { ApiService } from '../services/api.service';
import { ProgressRecord } from '../models/app.models';

@Component({
  selector: 'app-progress-page',
  template: `
    <section class="panel">
      <h2>Training progress</h2>
      <p>Employees can track completion across onboarding modules, SOP walkthroughs, and compliance checks.</p>
      <div class="record" *ngFor="let item of progress">
        <div>
          <strong>{{ item.module_name }}</strong>
          <p>{{ item.status }} · {{ item.completion_percent }}%</p>
        </div>
        <small>{{ item.notes }}</small>
      </div>
    </section>
  `,
  styles: [`
    .panel {
      max-width: 900px;
      margin: 0 auto;
      padding: 1.5rem;
      background: white;
      border-radius: 24px;
      box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
    }
    .record {
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem;
      border-radius: 16px;
      background: #f8fafc;
      margin-top: 1rem;
    }
    .record p {
      margin: 0.3rem 0 0;
      color: #475569;
    }
  `]
})
export class ProgressPageComponent implements OnInit {
  progress: ProgressRecord[] = [];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.progress().subscribe((data) => (this.progress = data));
  }
}
