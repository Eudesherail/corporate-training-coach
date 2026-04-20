import {DatePipe, NgOptimizedImage} from "@angular/common";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {NgModule} from "@angular/core";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {BrowserModule} from "@angular/platform-browser";
import {JwtModule} from "@auth0/angular-jwt";
import {PickerModule} from "@ctrl/ngx-emoji-mart";
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {AuthInterceptor} from "./_helper/auth.interceptor";
import {SafeUrlPipe} from "./_helper/safe-url.pipe";
import {AppRoutingModule} from "./app-routing.module";
import {AppComponent} from "./app.component";
import {AlertComponent} from "./components/alert/alert.component";
import {AuthCallbackComponent} from "./components/auth-callback/auth-callback.component";
import {ChatButtonComponent} from "./components/chat/chat-button/chat-button.component";
import {ChatHeaderComponent} from "./components/chat/chat-header/chat-header.component";
import {ChatMessageComponent} from "./components/chat/chat-message/chat-message.component";
import {ChatUserInputComponent} from "./components/chat/chat-user-input/chat-user-input.component";
import {EmojiFensterComponent} from "./components/chat/chat-user-input/emoji-fenster/emoji-fenster.component";
import {ChatWindowComponent} from "./components/chat/chat-window/chat-window.component";
import {BdsgGptComponent} from "./components/footer/bdsg-gpt/bdsg-gpt.component";
import {BdsgComponent} from "./components/footer/bdsg/bdsg.component";
import {FooterComponent} from "./components/footer/footer.component";
import {ImprintComponent} from "./components/footer/imprint/imprint.component";
import {SourceComponent} from "./components/footer/source/source.component";
import {GoalEditorComponent} from "./components/goal-editor/goal-editor.component";
import {HomeComponent} from "./components/home/home.component";
import {InformationsComponent} from "./components/informations/informations.component";
import {LoginFormComponent} from "./components/login-form/login-form.component";
import {NavbarComponent} from "./components/navbar/navbar.component";
import {RegisterFormComponent} from "./components/register-form/register-form.component";
import {AvatarCarouselComponent} from "./components/settings/avatar-carousel/avatar-carousel.component";
import {SettingsComponent} from "./components/settings/settings.component";
import { AdminComponent } from './components/admin/admin.component';
import { AdminUploadComponent } from './components/admin/admin-upload/admin-upload.component';
import { AdminEditComponent } from './components/admin/admin-edit/admin-edit.component';

export function tokenGetterFunction() {
    return localStorage.getItem("token");
}

@NgModule({
    declarations: [
        AppComponent,
        NavbarComponent,
        HomeComponent,
        LoginFormComponent,
        RegisterFormComponent,
        AlertComponent,
        ChatButtonComponent,
        ChatHeaderComponent,
        ChatMessageComponent,
        ChatUserInputComponent,
        ChatWindowComponent,
        SafeUrlPipe,
        SettingsComponent,
        GoalEditorComponent,
        AuthCallbackComponent,
        FooterComponent,
        ImprintComponent,
        BdsgComponent,
        SourceComponent,
        BdsgGptComponent,
        EmojiFensterComponent,
        AdminComponent,
        AdminUploadComponent,
        AdminEditComponent,
        InformationsComponent,
    ],
    imports: [
        BrowserModule,
        PickerModule,
        AppRoutingModule,
        HttpClientModule,
        NgbModule,
        FormsModule,
        ReactiveFormsModule,
        JwtModule.forRoot({
            config: {
                tokenGetter: () => {
                    return localStorage.getItem("token");
                },
                allowedDomains: ["localhost:8080", "stubu-app-paddy-90.cloud.okteto.net", "backend:8080", "stubu.oks.de"],
                disallowedRoutes: ["localhost:8080/home"],
            }
        }),
        AvatarCarouselComponent,
        NgOptimizedImage,
    ],
    providers: [
        {
            provide: HTTP_INTERCEPTORS,
            useClass: AuthInterceptor,
            multi: true
        },
        [DatePipe],
    ],
    bootstrap: [AppComponent]
})

export class AppModule {
}
