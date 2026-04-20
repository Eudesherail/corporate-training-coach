import {Component} from "@angular/core";
import {AuthService} from "./api/auth/auth.service";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"]
})

export class AppComponent {
  title = "studybuddy";

  constructor(private authService: AuthService) {
  }

  public isLoggedIn(): boolean {
    return this.authService.isAuthorized();
  }
}

