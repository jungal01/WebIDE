import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CodemirrorTextboxComponent } from './codemirror-textbox.component';

describe('CodemirrorTextboxComponent', () => {
  let component: CodemirrorTextboxComponent;
  let fixture: ComponentFixture<CodemirrorTextboxComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CodemirrorTextboxComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodemirrorTextboxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
