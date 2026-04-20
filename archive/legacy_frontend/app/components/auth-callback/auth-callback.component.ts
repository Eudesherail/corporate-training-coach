import {Component, OnInit} from "@angular/core";
import {ActivatedRoute, Router} from "@angular/router";
import {AuthService, OAuthState} from "../../api/auth/auth.service";


@Component({
    selector: "app-auth-callback",
    templateUrl: "./auth-callback.component.html",
    styleUrls: ["./auth-callback.component.scss"]
})
export class AuthCallbackComponent implements OnInit {

    constructor(
        private route: ActivatedRoute,
        private authService: AuthService,
        private router: Router
    ) {
    }

    ngOnInit() {
        this.route.queryParams.subscribe(params => {
            const {code, state} = params;
            console.log(code);

            const stateHandlerMap = {
                [OAuthState.GITHUB]: () => this.authService.fetchTokenFromCode(OAuthState.GITHUB, code),
                [OAuthState.INVITE]: () => this.authService.fetchTokenFromCode(OAuthState.INVITE, code),
                [OAuthState.MICROSOFT]: () => this.authService.fetchTokenFromCode(OAuthState.MICROSOFT, code)
            };

            const handler = stateHandlerMap[state as OAuthState];

            if (handler) {
                handler().subscribe(this.handleResponse);
            }
        });
    }


    private handleResponse = (response: any) => {
        localStorage.setItem("token", response.token);
        localStorage.setItem("userid", response.userId);
        localStorage.setItem("username", response.username);
        this.router.navigate(["/home"]).then();
    }
}
