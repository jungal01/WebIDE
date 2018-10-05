import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TextboxCOMPComponent } from './textbox-comp.component';

describe('TextboxCOMPComponent', () => {
  let component: TextboxCOMPComponent;
  let fixture: ComponentFixture<TextboxCOMPComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TextboxCOMPComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TextboxCOMPComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
