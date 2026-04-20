import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Injectable} from "@angular/core";
import {Observable} from "rxjs";
import {tap} from "rxjs/operators";
import {environment} from "../../../environments/environment";
import {Config} from "./config.model";

@Injectable({
    providedIn: "root"
})
export class ConfigService {
    private baseUrl = `${environment.backendUrl}/api/profile/`;

    constructor(private httpClient: HttpClient) {}

    private createHeaders(): HttpHeaders {
        const token = localStorage.getItem('token');
        return new HttpHeaders().set('Authorization', `Bearer ${token}`);
    }

    updateUserConfig(username: string, avatarname: string): Observable<Config> {
        const headers = this.createHeaders();
        const userId = localStorage.getItem("userid");
        console.debug(`Updating user config for user ${userId}.`);
        const userConfig = {username: username, avatarName: avatarname};
        return this.httpClient.put<Config>(`${this.baseUrl}`, userConfig, { headers: headers }).pipe(
            source => source.pipe(
                tap(conf => {
                    console.log(conf)
                    localStorage.setItem("username", conf.username);
                    localStorage.setItem("avatarname", conf.avatarname);
//                    localStorage.setItem("token", conf.token)
                })
            )
        );
    }
}
