import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { TextboxCOMPComponent } from './textbox-comp/textbox-comp.component';
import { CodemirrorTextboxComponent } from './codemirror-textbox/codemirror-textbox.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    TextboxCOMPComponent,
    CodemirrorTextboxComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
