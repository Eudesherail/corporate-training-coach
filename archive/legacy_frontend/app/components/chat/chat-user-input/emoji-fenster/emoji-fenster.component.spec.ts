import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmojiFensterComponent } from './emoji-fenster.component';

describe('EmojiFensterComponent', () => {
  let component: EmojiFensterComponent;
  let fixture: ComponentFixture<EmojiFensterComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [EmojiFensterComponent]
    });
    fixture = TestBed.createComponent(EmojiFensterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
