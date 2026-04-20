import {inject, NgModule} from "@angular/core";
import {RouterModule, Routes} from "@angular/router";
import {AuthService} from "./api/auth/auth.service";
import {ChatWindowComponent} from "./components/chat/chat-window/chat-window.component";
import {BdsgGptComponent} from "./components/footer/bdsg-gpt/bdsg-gpt.component";
import {BdsgComponent} from "./components/footer/bdsg/bdsg.component";
import {ImprintComponent} from "./components/footer/imprint/imprint.component";
import {SourceComponent} from "./components/footer/source/source.component";
import {GoalEditorComponent} from "./components/goal-editor/goal-editor.component";
import {HomeComponent} from "./components/home/home.component";
import {LoginFormComponent} from "./components/login-form/login-form.component";
import {RegisterFormComponent} from "./components/register-form/register-form.component";
import {SettingsComponent} from "./components/settings/settings.component";
import {AuthCallbackComponent} from "./components/auth-callback/auth-callback.component";

import {AdminComponent} from "./components/admin/admin.component";
import {AdminUploadComponent} from "./components/admin/admin-upload/admin-upload.component";
import {AdminEditComponent} from "./components/admin/admin-edit/admin-edit.component";

import {InformationsComponent} from "./components/informations/informations.component";

const isLoggedIn = () => inject(AuthService).canActivate();

const routes: Routes = [
    {path: "home", component: HomeComponent, canActivate: [isLoggedIn]},
    {path: "chat", component: ChatWindowComponent, canActivate: [isLoggedIn]},
    {path: "settings", component: SettingsComponent, canActivate: [isLoggedIn]},
    {path: "goal-editor", component: GoalEditorComponent, canActivate: [isLoggedIn]},
    {path: "admin-bereich", component: AdminComponent, canActivate: [isLoggedIn]},
    {path: "admin-bereich/upload", component: AdminUploadComponent, canActivate: [isLoggedIn]},
    {path: "admin-bereich/edit", component: AdminEditComponent, canActivate: [isLoggedIn]},
    {path: "informations", component: InformationsComponent},
    {path: "login", component: LoginFormComponent},
    //{path: "register", component: RegisterFormComponent},
    {path: "auth-callback", component: AuthCallbackComponent},
    {path: "imprint", component: ImprintComponent},
    {path: "dse", component: BdsgComponent},
    {path: "dse-gpt", component: BdsgGptComponent},
    {path: "source", component: SourceComponent},
    {path: "", redirectTo: "home", pathMatch: "full"},
];

@NgModule({
    imports: [RouterModule.forRoot(routes, {scrollPositionRestoration: 'enabled'})],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
