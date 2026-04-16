import { Component, computed, input } from '@angular/core';
import { ChartModule } from 'primeng/chart';
import { ChangeDetectionStrategy } from '@angular/core';
import { ChartData, ChartOptions } from 'chart.js';


/**
 *  Reusable chart component for displaying bar charts in the dashboard,
 *  take a chart data object as input and renders a bar chart with predefined options for styling and responsiveness.
 *  Allows for a single place to update styling and chart options 
 */
@Component({
  selector: 'app-barchartcomponent',
  imports: [ChartModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './barchartcomponent.html',
})
export class Barchartcomponent {

  chartData = input.required<ChartData<'bar'>>();


  chartOptions = computed<ChartOptions<'bar'>>(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: '#57534e',
          usePointStyle: true,
          boxWidth: 10,
          boxHeight: 10
        }
      },
      tooltip: {
        callbacks: {
          label: (context: any) => `${context.dataset.label}: ${context.parsed.y} MW`
        }
      }
    },
    scales: {
      x: {
        stacked: true,
        ticks: {
          color: '#57534e'
        },
        grid: {
          display: false
        },
        border: {
          display: false
        }
      },
      y: {
        stacked: true,
        beginAtZero: true,
        ticks: {
          color: '#57534e',
          callback: (value: string | number) => `${value} MW`
        },
        grid: {
          color: 'rgba(94, 11, 21, 0.08)'
        },
        border: {
          display: false
        }
      }
    }
  }));


}
