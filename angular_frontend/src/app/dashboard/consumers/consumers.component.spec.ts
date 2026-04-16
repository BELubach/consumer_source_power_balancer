
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ConsumersComponent } from './consumers.component';
import { DashboardStore } from '../dashboard.store';
import { signal } from '@angular/core';
import { vi } from 'vitest';

export const createMockStore = () => ({
  consumers: signal([]),
  sources: signal([]),
  loading: signal(false),
  error: signal(null),
  loadConsumers: vi.fn(),
  loadSources: vi.fn(),
});

describe('ConsumersComponent', () => {
  let component: ConsumersComponent;
  let fixture: ComponentFixture<ConsumersComponent>;
  let mockStore: ReturnType<typeof createMockStore>;

  beforeEach(async () => {
    mockStore = createMockStore();

    await TestBed.configureTestingModule({
      imports: [ConsumersComponent],
      providers: [
        { provide: DashboardStore, useValue: mockStore }
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ConsumersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges(); // Triggers ngOnInit and signals
  });

  it('should create and call loadConsumers', () => {
    expect(component).toBeTruthy();
    expect(mockStore.loadConsumers).toHaveBeenCalled();
  });

  it('should render an empty state initially', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    // The table body should be empty because consumers() is []
    expect(compiled.querySelectorAll('tbody tr').length).toBe(0);
  });
});