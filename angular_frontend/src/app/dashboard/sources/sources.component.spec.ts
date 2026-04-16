import { ComponentFixture, TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';
import { vi } from 'vitest';

import { SourcesComponent } from './sources.component';
import { DashboardStore } from '../dashboard.store';
import { Source } from './sources.models';

describe('SourcesComponent', () => {
  let component: SourcesComponent;
  let fixture: ComponentFixture<SourcesComponent>;
  let mockDashboardStore: {
    sources: ReturnType<typeof signal<Source[]>>;
    loadSources: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    mockDashboardStore = {
      sources: signal<Source[]>([]),
      loadSources: vi.fn(),
    };

    await TestBed.configureTestingModule({
      imports: [SourcesComponent],
      providers: [{ provide: DashboardStore, useValue: mockDashboardStore }],
    }).compileComponents();

    fixture = TestBed.createComponent(SourcesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load sources on init', () => {
    expect(mockDashboardStore.loadSources).toHaveBeenCalledTimes(1);
  });
});
