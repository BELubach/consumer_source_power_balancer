import { signal } from '@angular/core';
import { TestBed, ComponentFixture } from '@angular/core/testing';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { DashboardComponent } from './dashboard.component';
import { DashboardStore } from './dashboard.store';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async () => {
    const mockStore = {
      sources: signal([]),
      consumers: signal([]),
      loading: signal(false),
      error: signal(null),
      loadSources: vi.fn(),
      loadConsumers: vi.fn(),
    };

    await TestBed.configureTestingModule({
      imports: [DashboardComponent],
      providers: [
        { provide: DashboardStore, useValue: mockStore }
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});