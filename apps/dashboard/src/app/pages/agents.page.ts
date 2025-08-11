import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  standalone: true,
  selector: 'app-agents',
  imports: [CommonModule, FormsModule],
  template: `
  <h2>Agents</h2>
  <form (ngSubmit)="create()">
    <input [(ngModel)]="form.name" name="name" placeholder="Name" required />
    <input [(ngModel)]="form.type" name="type" placeholder="Type" />
    <select [(ngModel)]="form.mode" name="mode">
      <option value="approved">Approved</option>
      <option value="auto">Auto</option>
    </select>
    <input [(ngModel)]="form.model" name="model" placeholder="Model" />
    <button type="submit">Create</button>
  </form>

  <div style="margin-top:8px">
    <button (click)="run('Social Daily')">Run Social Daily</button>
    <button (click)="run('Theory Builder')">Run Theory Builder</button>
  </div>

  <table border="1" cellpadding="4" cellspacing="0" style="margin-top:8px; width:100%">
    <tr><th>Name</th><th>Type</th><th>Status</th><th>Mode</th><th>Model</th><th>Last Heartbeat</th><th>Actions</th></tr>
    <tr *ngFor="let a of agents">
      <td>{{a.name}}</td>
      <td>{{a.type}}</td>
      <td>{{a.status}}</td>
      <td>
        <select [ngModel]="a.mode" (ngModelChange)="setMode(a.id, $event)">
          <option value="approved">Approved</option>
          <option value="auto">Auto</option>
        </select>
      </td>
      <td>
        <input [ngModel]="a.model" (ngModelChange)="setModel(a.id, $event)" />
      </td>
      <td>{{a.last_heartbeat}}</td>
      <td>
        <button (click)="cmd(a.id,'start')">Start</button>
        <button (click)="cmd(a.id,'pause')">Pause</button>
        <button (click)="cmd(a.id,'stop')">Stop</button>
        <button (click)="cmd(a.id,'restart')">Restart</button>
      </td>
    </tr>
  </table>
  `
})
export class AgentsPage implements OnInit {
  api = inject(ApiService);
  agents: any[] = [];
  form = { name: '', type: 'social', mode: 'approved', model: 'llama3.1:8b' };

  ngOnInit(){
    this.reload();
    this.api.onAgentsChanged(_ => this.reload());
  }
  reload(){ this.api.listAgents().subscribe(a => this.agents = a); }
  create(){ this.api.createAgent(this.form).subscribe(() => this.reload()); }
  setMode(id:string, mode:string){ this.api.patchAgentConfig(id,{mode}).subscribe(() => this.reload()); }
  setModel(id:string, model:string){ this.api.patchAgentConfig(id,{model}).subscribe(() => this.reload()); }
  cmd(id:string, action:string){ this.api.agentCommand(id, action).subscribe(() => this.reload()); }
  run(name:string){ this.api.runWorkflow(name).subscribe(); }
}

