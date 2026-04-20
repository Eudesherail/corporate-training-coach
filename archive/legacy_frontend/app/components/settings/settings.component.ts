import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {environment} from "../../../environments/environment";
import {AlertService} from "../../_helper/alert.service";
import {ConfigService} from "../../api/config/config.service";

@Component({
    selector: "app-settings",
    templateUrl: "./settings.component.html",
    styleUrls: ["./settings.component.scss"]
})
export class SettingsComponent {
    username: string = "";
    avatarName: string = "";

    constructor(private http: HttpClient,
                private configService: ConfigService,
                private alertService: AlertService,
                private router: Router) {
        this.username = localStorage.getItem("username") ?? "dsa";
        this.avatarName = localStorage.getItem("avatarName") ?? "";
    }

    // Funktion zum Speichern der Benutzerkonfiguration
    public saveUserConfig(): void {
        this.configService.updateUserConfig(this.username, this.avatarName).subscribe(
            // Wird aufgerufen, wenn der Server erfolgreich antwortet
            () => {
                localStorage.setItem("username", this.username);
                localStorage.setItem("avatarName", this.avatarName)
                this.alertService.info('Benutzerkonfiguration wurde erfolgreich gespeichert.');
            },
            // Wird aufgerufen, wenn ein Fehler auftritt
            () => {
                this.alertService.warn('Ein Fehler ist aufgetreten beim Speichern der Benutzerkonfiguration.');
            }
        );
    }
    
    public deleteMessageHistory(): void {
        const token = localStorage.getItem('token');
        const header = new HttpHeaders().set('Authorization', `Bearer ${token}`);
        const apiUrl = `${environment.backendUrl}/api`;
        this.http.delete(`${apiUrl}/delete_messages/`, { headers: header }).subscribe(() => {
            this.alertService.info("Chatverlauf wurde gelöscht.");
            console.log("Chatverlauf wurde gelöscht.");
          },
          error => {
            console.error("Fehler beim Löschen des Chatverlaufs: ", error);
          }
        );
      }

    public cancel(): void {
        this.router.navigate(["/home"]).then();
    }
}
