import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Injectable} from "@angular/core";
import {Router} from "@angular/router";
import {JwtHelperService} from "@auth0/angular-jwt";
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";
import {AlertService} from "../../_helper/alert.service";
import { AuthResponse } from "./auth-response.model";

@Injectable({
    providedIn: "root"
})



export class AuthService {
    //private baseUrl = "https://stubu-app-paddy-90.cloud.okteto.net/api/auth";
    private baseUrl = `${environment.backendUrl}/api/auth`;
    private oauth2RedirectUri = encodeURIComponent('https://stubu.oks.de/auth-callback');


    private stateForMicrosoft = 'microsoft';
    private stateForGithub = 'github';
    private stateForInvite = 'inviteee';



    constructor(private httpClient: HttpClient,
                private jwtHelperService: JwtHelperService,
                private alertService: AlertService,
                private router: Router) {

    }

    public updateUserInfo() {
        const payload = {
            userId: Number(localStorage.getItem("userid")),
            goal: "test",
            telegramId: "test"
        };

        const token = localStorage.getItem("token");
        const headers = new HttpHeaders().set("Authorization", `Bearer ${token}`);

        return this.httpClient.put(`https://stubu-app-paddy-90.cloud.okteto.net/api/user/update`,
            payload,
            {headers: headers});
    }

    public signup(username: string, email: string, password: string): Observable<Object> {
        localStorage.clear();
        return this.httpClient.post(`${this.baseUrl}/signup`, {username, email, password});
    }

    public signin(email: string, password: string): Observable<Object> {
        localStorage.clear();
        if (localStorage.getItem("token"))
            localStorage.removeItem("token");
        return this.httpClient.post(`${this.baseUrl}/signin`, {email, password});
    }

    public isAuthorized(): boolean {
        const token = localStorage.getItem("token");
        return !!(token && !this.jwtHelperService.isTokenExpired(token));
    }

    public canActivate(): boolean {
        if (this.isAuthorized()) {
            return true;
        } else {
            this.alertService.error("You are not logged in!");
            this.router.navigate(["/login"]).then();
            return false;
        }
    }

    public tokenGetter(): string | null {
        return localStorage.getItem("token");
    }

    private getOAuth2Url(authEndpoint: string, clientId: string, scope: string, state?: string): string {
        return `${authEndpoint}?client_id=${clientId}&redirect_uri=${this.oauth2RedirectUri}&response_type=code&scope=${scope}${state ? `&state=${state}` : ''}`;
    }

    public startMicrosoftOAuth2Login(): void {
        const clientId = 'a5b11bf9-15c7-4f78-8853-61769e0a128f';
        const scope = 'openid profile email';
        const authEndpoint = 'https://login.microsoftonline.com/DEIN_DIRECTORY_ID/oauth2/v2.0/authorize';
        
        window.location.href = this.getOAuth2Url(authEndpoint, clientId, scope, this.stateForMicrosoft);
    }

    public startInviteOAuth2Login(): void {
        const clientId = '9165d217-faf6-45ca-80a1-c53c8ea97a58';
        const scope = 'openid email profile offline_access';
        const authEndpoint = 'https://auth-preview.invite-toolcheck.de/oauth2/auth';
        
        window.location.href = this.getOAuth2Url(authEndpoint, clientId, scope, this.stateForInvite);
    }

    public startGithubOAuth2Login(): void {
        const clientId = 'f7c3b49a14b20ab68f21';
        const scope = 'user:email';
        const authEndpoint = 'https://github.com/login/oauth/authorize';

        window.location.href = this.getOAuth2Url(authEndpoint, clientId, scope, this.stateForGithub);
    }

    // OAuth2 Token-Anforderung für Microsoft
    public fetchTokenFromCodeForMicrosoft(code: string): Observable<AuthResponse> {
        const payload = { code };
        return this.httpClient.post<AuthResponse>(`${this.baseUrl}/oauth2/microsoft`, payload);
    }

    // OAuth2 Token-Anforderung für Invite
    public fetchTokenFromCodeForInvite(code: string): Observable<AuthResponse> {
        const payload = { code };
        return this.httpClient.post<AuthResponse>(`${this.baseUrl}/oauth2/invite`, payload);
    }

    // OAuth2 Token-Anforderung für GitHub
    public fetchTokenFromCodeForGithub(code: string): Observable<AuthResponse> {
        const payload = { code };
        return this.httpClient.post<AuthResponse>(`${this.baseUrl}/oauth2/github`, payload);
    }

}
