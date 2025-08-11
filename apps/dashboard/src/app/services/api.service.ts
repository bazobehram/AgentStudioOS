import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private supabase: SupabaseClient;
  apiBase = (window as any).__env?.API_BASE || 'http://localhost:8001';
  supabaseUrl = (window as any).__env?.SUPABASE_URL || 'http://localhost:3001';
  supabaseAnonKey = (window as any).__env?.SUPABASE_ANON_KEY || 'local-dev-anon';

  constructor(){
    this.supabase = createClient(this.supabaseUrl, this.supabaseAnonKey);
  }

  // REST
  listAgents(){ return this.http.get<any[]>(`${this.apiBase}/agents`); }
  createAgent(body:any){ return this.http.post(`${this.apiBase}/agents`, body); }
  patchAgentConfig(id:string, body:any){ return this.http.patch(`${this.apiBase}/agents/${id}/config`, body); }
  agentCommand(id:string, action:string){ return this.http.post(`${this.apiBase}/agents/${id}/command`, {action}); }
  listTasks(){ return this.http.get<any[]>(`${this.apiBase}/tasks`); }
  createTask(body:any){ return this.http.post(`${this.apiBase}/tasks`, body); }
  listApprovals(){ return this.http.get<any[]>(`${this.apiBase}/approvals`); }
  patchApproval(id:string, body:any){ return this.http.patch(`${this.apiBase}/approvals/${id}`, body); }
  getLog(taskId:string){ return this.http.get<any>(`${this.apiBase}/logs/${taskId}`); }
  saveSecret(body:any){ return this.http.post(`${this.apiBase}/secrets`, body); }
  runWorkflow(name:string){ return this.http.post(`${this.apiBase}/workflows/run`, {name}); }

  // Realtime subscriptions
  onAgentsChanged(cb:(payload:any)=>void){
    return this.supabase.channel('public:agents')
      .on('postgres_changes', {event:'*', schema:'public', table:'agents'}, cb)
      .subscribe();
  }
  onTasksChanged(cb:(payload:any)=>void){
    return this.supabase.channel('public:tasks')
      .on('postgres_changes', {event:'*', schema:'public', table:'tasks'}, cb)
      .subscribe();
  }
  onApprovalsChanged(cb:(payload:any)=>void){
    return this.supabase.channel('public:approvals')
      .on('postgres_changes', {event:'*', schema:'public', table:'approvals'}, cb)
      .subscribe();
  }
}

