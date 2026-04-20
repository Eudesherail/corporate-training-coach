import {HttpClient} from "@angular/common/http";
import {Injectable} from "@angular/core";
import {Router} from "@angular/router";
import {JwtHelperService} from "@auth0/angular-jwt";
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";
import {AlertService} from "../../_helper/alert.service";
import {AuthResponse} from "./auth-response.model";

// OAuth state enum
export enum OAuthState {
    MICROSOFT = "microsoft",
    GITHUB = "github",
    INVITE = "inviteee"
}

@Injectable({
    providedIn: "root"
})


export class AuthService {
    private baseUrl = `${environment.backendUrl}/api`;
    private oauth2RedirectUri = encodeURIComponent("https://stubu.oks.de/auth-callback");


    constructor(
        private httpClient: HttpClient,
        private jwtHelperService: JwtHelperService,
        private alertService: AlertService,
        private router: Router
    ) {
    }


    // Method for signup
    public signup(username: string, email: string, password: string): Observable<Object> {
        this.clearToken();
        return this.httpClient.post(`${this.baseUrl}/signup/`, { username, email, password });
    }

    // Method for signin
    public signin(email: string, password: string): Observable<Object> {
        this.clearToken();
        return this.httpClient.post(`${this.baseUrl}/signin/`, {email, password});
    }

    // Check if user is authorized
    public isAuthorized(): boolean {
        const token = this.tokenGetter();
        return !!(token && !this.jwtHelperService.isTokenExpired(token));
    }

    // Check if user can activate something (like a route)
    public canActivate(): boolean {
        if (this.isAuthorized()) {
            return true;
        } else {
            this.router.navigate(["/login"]).then();
            return false;
        }
    }

    // Get stored token
    public tokenGetter(): string | null {
        return localStorage.getItem("token");
    }

    private clearToken() {
        localStorage.removeItem("token");
    }

    private getOAuth2Url(authEndpoint: string, clientId: string, scope: string, state?: OAuthState): string {
        return `${authEndpoint}?client_id=${clientId}&redirect_uri=${this.oauth2RedirectUri}&response_type=code&scope=${scope}${state ? `&state=${state}` : ""}`;
    }

    // Unified OAuth2 login starter
    public startOAuth2Login(platform: OAuthState): void {
        const configs = {
            [OAuthState.MICROSOFT]: {
                clientId: "a5b11bf9-15c7-4f78-8853-61769e0a128f",
                scope: "openid profile email",
                authEndpoint: "https://login.microsoftonline.com/DEIN_DIRECTORY_ID/oauth2/v2.0/authorize"
            },
            [OAuthState.GITHUB]: {
                clientId: "f7c3b49a14b20ab68f21",
                scope: "user:email",
                authEndpoint: "https://github.com/login/oauth/authorize"
            },
            [OAuthState.INVITE]: {
                clientId: "a72e8cd0-99a0-4934-881c-cc34137c805e",
                scope: "openid email profile offline_access",
                authEndpoint: "https://auth.invite-toolcheck.de/oauth2/auth"
            }
        };

        const config = configs[platform];
        window.location.href = this.getOAuth2Url(config.authEndpoint, config.clientId, config.scope, platform);
    }

    // Fetch OAuth2 token using code
    public fetchTokenFromCode(platform: OAuthState, code: string): Observable<AuthResponse> {
        const payload = { inviteCode: code };
        return this.httpClient.post<AuthResponse>(`${this.baseUrl}/${platform}`, payload);
    }
}
