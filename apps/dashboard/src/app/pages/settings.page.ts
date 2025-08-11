import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  standalone: true,
  selector: 'app-settings',
  imports: [CommonModule, FormsModule],
  template: `
  <h2>Settings</h2>
  <form (ngSubmit)="save()">
    <input [(ngModel)]="form.key" name="key" placeholder="Key (e.g., X_API_KEY)" required />
    <input [(ngModel)]="form.value" name="value" placeholder="Value" required />
    <input [(ngModel)]="form.scope" name="scope" placeholder="Scope" />
    <button type="submit">Save Secret</button>
  </form>
  <p>{{ savedMsg }}</p>
  `
})
export class SettingsPage {
  api = inject(ApiService);
  form = { key: '', value: '', scope: '' };
  savedMsg = '';
  save(){ this.api.saveSecret(this.form).subscribe(_ => this.savedMsg = 'Saved'); }
}

