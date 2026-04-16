import { Injectable, inject, signal } from '@angular/core';
import { ConsumerApi } from './consumers/consumers.api';
import { Consumer } from './consumers/consumers.models';
import { ToggleConsumerPowerRequirementRequest } from './consumers/consumers.models';
import { Source } from './sources/sources.models';
import { SourcesApi } from './sources/sources.api';


/**
 * Service class that loads and holds state for the dashboard, 
 * Consumer and source data is called from the api and stored in signals
 * This class is supposed to be injected in a component that needs the data, 
 * and the component can then subscribe to the signals to get updates when the data changes.
 */
@Injectable({ providedIn: 'root' })
export class DashboardStore {

  private api = inject(ConsumerApi);
  private sourcesApi = inject(SourcesApi);

  readonly consumers = signal<Consumer[]>([]);
  readonly sources = signal<Source[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  loadConsumers() {
    this.loading.set(true);

    this.api.getConsumers().subscribe({
      next: (data) => {
        this.consumers.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Failed to load consumers');
        this.loading.set(false);
      }
    });
  }

  deactivateConsumer(id: number, request: ToggleConsumerPowerRequirementRequest) {
    this.api.deactivateConsumer(id, request).subscribe({
      next: () => {
        this.loadConsumers(); 
      },
      error: () => {
        this.error.set('Failed to update consumer');
      }
    });
  }

  loadSources() {
    this.sourcesApi.getSources().subscribe({
      next: (data) => {
        this.sources.set(data);
      }
    });


  }
}