import { Component, computed, signal, inject, OnInit } from '@angular/core';
import { ChangeDetectionStrategy } from '@angular/core';
import { DashboardStore } from '../dashboard.store';
import { Barchartcomponent } from "../barchartcomponent/barchartcomponent";
import { ChartData } from 'chart.js';
import { RadioButtonModule } from 'primeng/radiobutton';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-sources',
  templateUrl: './sources.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './sources.component.css',
  imports: [Barchartcomponent, RadioButtonModule, FormsModule]
})
export class SourcesComponent implements OnInit {
  private store = inject(DashboardStore);

  sources = this.store.sources;

  selectedDataset = signal<'capacity' | 'requestedPower'>('capacity');

  ngOnInit() {
    this.store.loadSources();
  }

  requestedPowerChartData = computed(() => ({
    labels: this.sources().map(source => source.name),
    datasets: [
      {
        label: 'Requested Power (MW)',
        data: this.sources().map(source => source.requested_power),
        borderWidth: 1
      }
    ]
  }));

  capacityChartData = computed(() => ({
    labels: this.sources().map(source => source.name),
    datasets: [
      {
        label: 'Capacity (MW)',
        data: this.sources().map(source => source.capacity),
        borderWidth: 1
      }
    ]
  }));

  // Return the appropriate chart data based on the selected dataset
  chartData = computed<ChartData<'bar'>>(() => {
    const selected = this.selectedDataset();
    
    if (selected === 'requestedPower') {
      return this.requestedPowerChartData();
    }

    if (selected === 'capacity') {
      return this.capacityChartData();
    }

    return this.capacityChartData(); 
  });

}



