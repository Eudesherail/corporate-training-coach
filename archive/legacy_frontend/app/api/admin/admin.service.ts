import { Injectable} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {environment} from "../../../environments/environment";
import { Observable, map } from 'rxjs';
import { UserService } from '../user/user.service';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  constructor(private http: HttpClient) { }
  private baseUrl = `${environment.backendUrl}/api/Admin`;
  saveDocument(dokumentDaten: FormData):  Observable<any> {
    return this.http.post(`${this.baseUrl}/upload/`, dokumentDaten,{ responseType: 'text' });
    }
  changeDocument(dokumentDaten: FormData):  Observable<any> {
    return this.http.post(`${this.baseUrl}/edit/`, dokumentDaten,{ responseType: 'text' });
  }

  getDocument(): Observable<any>{
    return this.http.get(`${this.baseUrl}/laden/${localStorage.getItem("username")}/`);
  }
  deleteDocuments(id:  any): Observable<any>{
    return this.http.delete(`${this.baseUrl}/loeschen/${id}/`,{ responseType: 'text' });
  }

  
}
