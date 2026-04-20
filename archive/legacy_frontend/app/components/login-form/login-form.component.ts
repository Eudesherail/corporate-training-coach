import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {AuthService, OAuthState} from "../../api/auth/auth.service";
import {AlertService} from "../../_helper/alert.service";

@Component({
  selector: "app-login-form",
  templateUrl: "./login-form.component.html",
  styleUrls: ["./login-form.component.scss"]
})
export class LoginFormComponent {
  email: string = "";
  password: string = "";
  OAuthState = OAuthState;

  constructor(private authService: AuthService, private router: Router, private alertService: AlertService) {
  }

  public signin(): void {
    if (!this.email || !this.password) {
      this.alertService.error("Alle Felder müssen ausgefüllt werden.");
      return;
    }

    this.authService.signin(this.email, this.password).subscribe(
      
      (json: any) => {
        console.log(json)
        localStorage.setItem("token", json.access);
        console.log('Token stored:', json.access);
        localStorage.setItem("userid", json.userId);
        localStorage.setItem("username", json.username);
        localStorage.setItem("avatarName", json.avatarName);
        localStorage.setItem("is_superuser", json.is_superuser);
        this.router.navigate(["/home"]).then();
        
      },
      error => {
        if (error.status === 400) {
            this.alertService.error(error.error.message); // Die vom Backend gesendete Fehlermeldung anzeigen
        } else {
            this.alertService.error("Ein unbekannter Fehler ist aufgetreten.");
        }
      }
    );
}


    // Funktionen zum Starten der OAuth2-Anmeldung
  public startOAuth2Login(state: OAuthState): void {
      this.authService.startOAuth2Login(state);
  }
}
