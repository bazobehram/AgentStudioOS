import { Routes } from '@angular/router';
import { AgentsPage } from './pages/agents.page';
import { TasksPage } from './pages/tasks.page';
import { ApprovalsPage } from './pages/approvals.page';
import { LogsPage } from './pages/logs.page';
import { SettingsPage } from './pages/settings.page';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'agents' },
  { path: 'agents', component: AgentsPage },
  { path: 'tasks', component: TasksPage },
  { path: 'approvals', component: ApprovalsPage },
  { path: 'logs', component: LogsPage },
  { path: 'settings', component: SettingsPage },
];

