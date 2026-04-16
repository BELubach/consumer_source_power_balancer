import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChartData } from 'chart.js';
import { Barchartcomponent } from './barchartcomponent';

const MOCK_CHART_DATA: ChartData<'bar'> = {
  labels: ['Hospital', 'Train station', 'Market'],
  datasets: [
    { label: 'Requested Power', data: [230, 180, 300], backgroundColor: '#f59e0b' },
  ],
};

describe('Barchartcomponent', () => {
  let component: Barchartcomponent;
  let fixture: ComponentFixture<Barchartcomponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Barchartcomponent],
    })
      .compileComponents();

    fixture = TestBed.createComponent(Barchartcomponent);
    component = fixture.componentInstance;
    fixture.componentRef.setInput('chartData', MOCK_CHART_DATA);
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('test load mock chart data', () => {
    expect(component.chartData()).toEqual(MOCK_CHART_DATA);
  });


  it('should format tooltip labels with MW unit', () => {
    const tooltip = component.chartOptions().plugins?.tooltip;
    const labelFn = tooltip?.callbacks?.label as ((ctx: any) => string) | undefined;
    const label = labelFn?.({ dataset: { label: 'Solar' }, parsed: { y: 42 } });
    expect(label).toBe('Solar: 42 MW');
  });

  it('should format y-axis ticks with MW unit', () => {
    const scales = component.chartOptions().scales as any;
    const tickValue = scales['y'].ticks.callback(100);
    expect(tickValue).toBe('100 MW');
  });

  it('should recompute options when chartData input changes', () => {
    const updatedData: ChartData<'bar'> = {
      labels: ['Hospital', 'Train station', 'Market'],
      datasets: [ { label: 'Available Power', data: [50, 150, 250], backgroundColor: '#3b82f6' },],
    };
    fixture.componentRef.setInput('chartData', updatedData);
    fixture.detectChanges();

    expect(component.chartData()).toEqual(updatedData);
    // chartOptions is a computed; verify it still resolves correctly
    expect(component.chartOptions().responsive).toBe(true);
  });
});
