import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  standalone: true,
  selector: 'app-tasks',
  imports: [CommonModule, FormsModule],
  template: `
  <h2>Tasks</h2>
  <form (ngSubmit)="enqueue()">
    <input [(ngModel)]="form.agent_id" name="agent_id" placeholder="Agent ID" required />
    <select [(ngModel)]="form.type" name="type">
      <option>draft_post</option>
      <option>post_x</option>
      <option>post_bsky</option>
      <option>browser_screenshot</option>
      <option>store_note</option>
    </select>
    <input [(ngModel)]="form.payload" name="payload" placeholder='{"prompt":"Write"}' />
    <button type="submit">Enqueue</button>
  </form>
  <pre>{{ tasks | json }}</pre>
  `
})
export class TasksPage implements OnInit {
  api = inject(ApiService);
  tasks: any[] = [];
  form = { agent_id: '', type: 'draft_post', payload: '{"prompt":"Write a short post"}' };

  ngOnInit(){
    this.reload();
    this.api.onTasksChanged(_ => this.reload());
  }
  reload(){ this.api.listTasks().subscribe(t => this.tasks = t); }
  enqueue(){
    const body = { agent_id: this.form.agent_id, type: this.form.type, payload: JSON.parse(this.form.payload || '{}') };
    this.api.createTask(body).subscribe(_ => this.reload());
  }
}

