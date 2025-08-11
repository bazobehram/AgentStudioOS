import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  standalone: true,
  selector: 'app-logs',
  imports: [CommonModule, FormsModule],
  template: `
  <h2>Logs</h2>
  Task ID: <input [(ngModel)]="taskId"/> <button (click)="load()">Load</button>
  <pre>{{ content }}</pre>
  `
})
export class LogsPage {
  api = inject(ApiService);
  taskId = '';
  content = '';
  load(){ this.api.getLog(this.taskId).subscribe({next: j => this.content = j.content, error: _ => this.content = 'Not found'}); }
}

