import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AdminPageComponent } from './pages/admin-page.component';
import { AssistantPageComponent } from './pages/assistant-page.component';
import { EmployeePageComponent } from './pages/employee-page.component';
import { LoginPageComponent } from './pages/login-page.component';
import { ProgressPageComponent } from './pages/progress-page.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginPageComponent,
    AdminPageComponent,
    EmployeePageComponent,
    AssistantPageComponent,
    ProgressPageComponent,
  ],
  imports: [BrowserModule, HttpClientModule, FormsModule, AppRoutingModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
