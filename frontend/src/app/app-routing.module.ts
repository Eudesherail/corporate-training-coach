import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { authGuard } from './services/auth.guard';
import { AdminPageComponent } from './pages/admin-page.component';
import { AssistantPageComponent } from './pages/assistant-page.component';
import { EmployeePageComponent } from './pages/employee-page.component';
import { LoginPageComponent } from './pages/login-page.component';
import { ProgressPageComponent } from './pages/progress-page.component';

const routes: Routes = [
  { path: 'login', component: LoginPageComponent },
  { path: 'admin', component: AdminPageComponent, canActivate: [authGuard] },
  { path: 'employee', component: EmployeePageComponent, canActivate: [authGuard] },
  { path: 'assistant', component: AssistantPageComponent, canActivate: [authGuard] },
  { path: 'progress', component: ProgressPageComponent, canActivate: [authGuard] },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
