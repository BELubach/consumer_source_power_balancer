import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConsumersComponent } from './consumers/consumers.component';
import { SourcesComponent } from './sources/sources.component';
import { ChangeDetectionStrategy, OnInit, inject, signal } from '@angular/core';

import { DashboardStore } from './dashboard.store';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, ConsumersComponent, SourcesComponent],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {

  private store = inject(DashboardStore);

  tabToShow = signal<string | null>('sources');
  consumers = this.store.consumers;
  loading = this.store.loading;

  ngOnInit() {
    this.store.loadConsumers();
  }

}
