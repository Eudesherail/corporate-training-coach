import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {AlertService} from "../../_helper/alert.service";
import {AuthService} from "../../api/auth/auth.service";

@Component({
  selector: "app-register-form",
  templateUrl: "./register-form.component.html",
  styleUrls: ["./register-form.component.scss"]
})
export class RegisterFormComponent {
  username: string = "";
  email: string = "";
  password: string = "";

  constructor(private authService: AuthService, private router: Router, private alertService: AlertService) {
  }

  public signup(): void {
    if (!this.username || !this.email || !this.password) {
      this.alertService.error("Alle Felder müssen ausgefüllt werden.");
      return;
    }
  
    if (this.password.length < 8) {
      this.alertService.error("Passwort muss mindestens 8 Zeichen lang sein.");
      return;
    }
  
    const emailPattern = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/;
    if (!emailPattern.test(this.email)) {
      this.alertService.error("Bitte gib eine echt e-Mail Adresse ein.");
      return;
    }
    console.log(this.username, this.email, this.password)
    this.authService.signup(this.username, this.email, this.password).subscribe(
      (json: any) => {
        console.log(json)
        localStorage.setItem("token", json.token);
        localStorage.setItem("userid", json.userId);
        localStorage.setItem("username", json.username);
        localStorage.setItem("avatarName", json.avatarName);
        this.alertService.info("Registrierung erfolgreich!")
        this.router.navigate(["/home"]).then();
      },
      (error) => {
        console.log(error)
        console.error(error.error);
        this.alertService.error(error.error.message);
      }
    );
  }
}
