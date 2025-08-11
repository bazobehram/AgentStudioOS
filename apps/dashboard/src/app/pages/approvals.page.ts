import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  standalone: true,
  selector: 'app-approvals',
  imports: [CommonModule, FormsModule],
  template: `
  <h2>Approvals</h2>
  <div *ngFor="let a of approvals" style="border:1px solid #ccc; padding:8px; margin:4px;">
    <pre>{{ a | json }}</pre>
    <button (click)="approve(a.id)">Approve</button>
    <button (click)="reject(a.id)">Reject</button>
  </div>
  `
})
export class ApprovalsPage implements OnInit {
  api = inject(ApiService);
  approvals: any[] = [];
  ngOnInit(){
    this.reload();
    this.api.onApprovalsChanged(_ => this.reload());
  }
  reload(){ this.api.listApprovals().subscribe(a => this.approvals = a); }
  approve(id:string){ this.api.patchApproval(id,{status:'approved'}).subscribe(_=>this.reload()); }
  reject(id:string){ this.api.patchApproval(id,{status:'rejected'}).subscribe(_=>this.reload()); }
}

