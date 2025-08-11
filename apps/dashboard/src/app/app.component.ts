import { Component, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MatToolbarModule, MatButtonModule, MatIconModule, MatTabsModule],
  template: `
  <mat-toolbar color="primary">
    <span>AgentStudioOS</span>
    <span style="flex:1"></span>
    <button mat-button routerLink="/agents">Agents</button>
    <button mat-button routerLink="/tasks">Tasks</button>
    <button mat-button routerLink="/approvals">Approvals</button>
    <button mat-button routerLink="/logs">Logs</button>
    <button mat-button routerLink="/settings">Settings</button>
  </mat-toolbar>
  <router-outlet></router-outlet>
  `
})
export class AppComponent {}

