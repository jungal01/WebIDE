import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { TextboxCOMPComponent } from './textbox-comp/textbox-comp.component';
import { HeaderTabsComponent } from './header-tabs/header-tabs.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    TextboxCOMPComponent,
    HeaderTabsComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
