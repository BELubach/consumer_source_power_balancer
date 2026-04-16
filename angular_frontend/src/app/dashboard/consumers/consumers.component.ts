import { ChangeDetectionStrategy, Component, computed, inject, OnInit } from '@angular/core';
import type { ChartData } from 'chart.js';
import { Consumer, ToggleConsumerPowerRequirementRequest, RequiredPower } from './consumers.models';
import { FormsModule } from '@angular/forms';
import { CheckboxModule } from 'primeng/checkbox';
import { DashboardStore } from '../dashboard.store';
import { Barchartcomponent } from "../barchartcomponent/barchartcomponent";


@Component({
  selector: 'app-consumers',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './consumers.component.html',
  styleUrl: './consumers.component.css',
  imports: [CheckboxModule, FormsModule, Barchartcomponent]
})
export class ConsumersComponent implements OnInit {

  private store = inject(DashboardStore);

  consumers = this.store.consumers;
  loading = this.store.loading;

  ngOnInit() {
    this.store.loadConsumers();
  }

  isConsumerActive(consumer: Consumer): boolean {
    return this.getRequiredPower(consumer).some((r) => r.is_active !== false);
  }

  getRequiredPower(consumer: Consumer & { required_power?: RequiredPower[] }): RequiredPower[] {
    return consumer.requiredPower ?? consumer.required_power ?? [];
  }

  onConsumerToggle(consumer: Consumer, isActive: boolean) {
    const request: ToggleConsumerPowerRequirementRequest = {
      is_active: isActive
    };
    this.store.deactivateConsumer(consumer.id, request);
  }

  chartData = computed<ChartData<'bar'>>(() => (
    {

      labels: this.consumers().map((consumer) => consumer.name),
      datasets: [
        {
          label: 'Required power',
          data: this.consumers().map((consumer) => {
            const total = consumer.active_power ?? 0;
            return total;
          }),
          
        }
      ]
    }));

    tableData = computed(() => {
      return this.consumers().map(consumer => ({
        name: consumer.name,
        priority: consumer.priority,
        requiredPower: this.getRequiredPower(consumer).reduce((sum, rp) => sum + (rp.is_active ? rp.capacity : 0), 0),
        activePower: consumer.active_power ?? 0,
        isActive: this.isConsumerActive(consumer)
      }));
    });

}

