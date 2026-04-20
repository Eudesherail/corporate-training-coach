import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {AuthService} from "../../api/auth/auth.service";

@Component({
    selector: "app-navbar",
    templateUrl: "./navbar.component.html",
    styleUrls: ["./navbar.component.scss"]
})
export class NavbarComponent {
    is_superuser = localStorage.getItem('is_superuser');
    
    constructor(private router: Router, private authService: AuthService) {
        console.log("is_superuser:" + this.is_superuser);
    }

    public isLoggedIn(): boolean {
        return this.authService.isAuthorized();
    }

    public logout(): void {
        localStorage.removeItem("token");
        localStorage.clear();
        this.router.navigate(["/login"]).then();
    }
}
