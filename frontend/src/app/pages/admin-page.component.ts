import { Component, OnInit } from '@angular/core';

import { ApiService } from '../services/api.service';
import { DocumentItem } from '../models/app.models';

@Component({
  selector: 'app-admin-page',
  template: `
    <section class="grid">
      <article class="panel">
        <h2>Admin dashboard</h2>
        <div class="metrics" *ngIf="dashboard">
          <div><strong>{{ dashboard.total_documents }}</strong><span>Documents</span></div>
          <div><strong>{{ dashboard.total_quizzes }}</strong><span>Quizzes</span></div>
          <div><strong>{{ dashboard.total_employees }}</strong><span>Employees</span></div>
          <div><strong>{{ dashboard.active_progress_records }}</strong><span>Active progress items</span></div>
        </div>
      </article>

      <article class="panel">
        <h2>Upload internal document</h2>
        <form (ngSubmit)="upload()">
          <input [(ngModel)]="title" name="title" placeholder="Employee handbook" required />
          <input [(ngModel)]="category" name="category" placeholder="onboarding / sop / policy" required />
          <textarea [(ngModel)]="description" name="description" rows="3" placeholder="What should employees use this document for?"></textarea>
          <input type="file" accept="application/pdf" (change)="onFileChange($event)" required />
          <button type="submit">Upload and index PDF</button>
        </form>
        <p class="hint" [class.error]="uploadError">{{ uploadStatus }}</p>
      </article>

      <article class="panel">
        <h2>Indexed documents</h2>
        <div class="list" *ngIf="documents.length; else noDocs">
          <div class="item" *ngFor="let doc of documents">
            <div>
              <strong>{{ doc.title }}</strong>
              <p>{{ doc.category }} · {{ doc.total_pages }} pages</p>
            </div>
            <button type="button" (click)="generateQuiz(doc)">Generate quiz</button>
          </div>
        </div>
        <ng-template #noDocs>
          <p>No onboarding or policy documents indexed yet.</p>
        </ng-template>
      </article>

      <article class="panel">
        <h2>Employee roster</h2>
        <ul>
          <li *ngFor="let user of users">{{ user.full_name }} · {{ user.role }}</li>
        </ul>
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
      display: grid;
      gap: 1rem;
    }
    .metrics {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem;
    }
    .metrics div, .item {
      padding: 1rem;
      border-radius: 16px;
      background: #f8fafc;
    }
    form {
      display: grid;
      gap: 0.8rem;
    }
    input, textarea, button {
      padding: 0.9rem 1rem;
      border-radius: 14px;
      border: 1px solid #cbd5e1;
      font: inherit;
    }
    button {
      border: none;
      background: #2563eb;
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
    .item {
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      align-items: center;
    }
    .item p, .hint {
      margin: 0;
      color: #475569;
    }
    .hint.error {
      color: #b91c1c;
      font-weight: 600;
    }
    @media (max-width: 900px) {
      .grid { grid-template-columns: 1fr; }
    }
  `]
})
export class AdminPageComponent implements OnInit {
  dashboard: any;
  documents: DocumentItem[] = [];
  users: any[] = [];
  title = '';
  category = 'onboarding';
  description = '';
  selectedFile?: File;
  uploadError = false;
  uploadStatus = 'Admin can upload employee handbooks, SOPs, compliance guides, and policy manuals.';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.api.adminDashboard().subscribe((data) => (this.dashboard = data));
    this.api.documents().subscribe((data) => (this.documents = data));
    this.api.users().subscribe((data) => (this.users = data));
  }

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFile = input.files?.[0] ?? undefined;
    this.uploadError = false;
  }

  upload(): void {
    const trimmedTitle = this.title.trim();
    const trimmedCategory = this.category.trim();

    if (!trimmedTitle) {
      this.uploadError = true;
      this.uploadStatus = 'Enter a document title before uploading.';
      return;
    }

    if (!trimmedCategory) {
      this.uploadError = true;
      this.uploadStatus = 'Enter a document category before uploading.';
      return;
    }

    if (!this.selectedFile) {
      this.uploadError = true;
      this.uploadStatus = 'Choose a PDF file before uploading.';
      return;
    }

    if (!this.selectedFile.name.toLowerCase().endsWith('.pdf')) {
      this.uploadError = true;
      this.uploadStatus = 'Only PDF files are supported for indexing right now.';
      return;
    }

    this.uploadError = false;
    const formData = new FormData();
    formData.append('title', trimmedTitle);
    formData.append('category', trimmedCategory);
    formData.append('description', this.description || '');
    formData.append('file', this.selectedFile);

    this.api.uploadDocument(formData).subscribe({
      next: (doc) => {
        this.uploadStatus = `${doc.title} uploaded and chunked for retrieval.`;
        this.title = '';
        this.description = '';
        this.selectedFile = undefined;
        this.uploadError = false;
        this.load();
      },
      error: () => {
        this.uploadError = true;
        this.uploadStatus = 'Upload failed. Confirm the title, category, and PDF file, then try again.';
      },
    });
  }

  generateQuiz(doc: DocumentItem): void {
    this.api.generateQuiz(doc.id, `${doc.title} Knowledge Check`).subscribe(() => {
      this.uploadStatus = `Quiz generated from ${doc.title}.`;
      this.load();
    });
  }
}
