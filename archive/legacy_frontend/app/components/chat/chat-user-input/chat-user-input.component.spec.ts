import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatUserInputComponent } from './chat-user-input.component';

describe('ChatUserInputComponent', () => {
  let component: ChatUserInputComponent;
  let fixture: ComponentFixture<ChatUserInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChatUserInputComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatUserInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
