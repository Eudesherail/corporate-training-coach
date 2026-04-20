import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminService } from 'src/app/api/admin/admin.service';
import {AlertService} from "../../../_helper/alert.service";

@Component({
  selector: 'app-admin-upload',
  templateUrl: './admin-upload.component.html',
  styleUrls: ['./admin-upload.component.scss']
})
export class AdminUploadComponent {
  institutions = ["AKAD University", "Oskar Kämmer Schule", "TU Braunschweig"]
  selectedFile: File | null = null;

  onFileSelected(event: any): void {
    const fileInput = event.target;
    //ich kann das für mehere Files Anpassen! in dem Fall sollte ich dann unten für jedes Dokument das FormData überschreiben und sooft den Post machen bis es keine 
    //Docs mehr gibt
    this.selectedFile = event.target.files[0] as File;

    //reset file at wrong type
    if (!this.selectedFile.type.includes("pdf")) {
      this.alertService.warn("Bitte wählen Sie nur PDF-Dateien aus")
      this.selectedFile = null;
      fileInput.value = null;
    }

  }

  dokumentDaten: FormGroup;
  constructor(private fb: FormBuilder, private AdminService: AdminService, private alertService: AlertService) {
    this.dokumentDaten = this.fb.group({
      institution: ['', Validators.required],
      modul: ['', Validators.required],
      description: ['', Validators.required],
      document: [null, Validators.required]
    });
  }
  onSubmit() {
    
    //check for missing information
    if (this.dokumentDaten.invalid) {
      this.alertService.warn("Bitte füllen Sie alle Felder aus")
      return
    }
    
    const institution = this.dokumentDaten.get('institution');
    const modul = this.dokumentDaten.get('modul');
    const description = this.dokumentDaten.get('description');
    const document = this.selectedFile;
    const user_name = localStorage.getItem("username");
    console.log(user_name);
    
    if (institution && modul && description && document && user_name) {
      const formData = new FormData();
      formData.append('institution', institution.value);
      formData.append('modul', modul.value);
      formData.append('description', description.value);
      formData.append('document', document);
      formData.append('userName', user_name)
      //

      this.AdminService.saveDocument(formData).subscribe(
        response => {
          if (response.includes("Das Dokument wurde erfolgreich Hochgeladen :")) {
            this.alertService.info("Datei wurde erfolgreich hochgeladen");
            this.dokumentDaten.reset();
          } else if(response.includes("Die Datei existiert bereits.")) {
            this.alertService.info("Die Datei existiert bereits.");
          } else {
            console.error('Fehler bei der Anfrage: Ungültige Antwort');
          }
        },
        error => {
          this.alertService.warn("Beim Hochladen der Datei ist ein Fehler aufgetreten");
          console.error('Fehler beim Hochladen der Datei:', error);
        }
      );
    }
  }
}