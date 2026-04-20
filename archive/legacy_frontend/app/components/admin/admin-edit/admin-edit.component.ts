import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule } from '@angular/forms';
import { AdminService } from 'src/app/api/admin/admin.service';
import {AlertService} from "../../../_helper/alert.service";
@Component({
  selector: 'app-admin-edit',
  templateUrl: './admin-edit.component.html',
  styleUrls: ['./admin-edit.component.scss']
})
export class AdminEditComponent {
  institutions = ["AKAD University", "Oskar Kämmer Schule", "TU Braunschweig"];
  documents: any;
  dokumentDaten: FormGroup;
  selectedFile: any;
  isFileSelected: boolean = false;
  selectedId!: number;
  selectEdit: boolean = false;

ngOnInit(){
  this.getAllUserDataInfo();
}

constructor (private fb: FormBuilder, private AdminService: AdminService, private alertService: AlertService,){
  this.dokumentDaten = this.fb.group({
    institution: [''],
    modul: [''],
    description: [''],
    document: [null]
  });
 }

 onSubmit(documentAll:any) {
  const institution = this.dokumentDaten.get('institution');
  const modul = this.dokumentDaten.get('modul');
  const description = this.dokumentDaten.get('description');
  const document = this.selectedFile;
  const userName = documentAll.userName;
  const id = documentAll.id;
  if (institution && modul && description) {
    console.log("wird geschickt");
    const formData = new FormData();
    formData.append('institution', institution.value);
    formData.append('modul', modul.value);
    formData.append('description', description.value);
    formData.append('document', document);
    formData.append('userName', userName);
    formData.append('id', id)
    //
    
    this.AdminService.changeDocument(formData).subscribe(
      response => {
        if (response.includes("Erfolgreich aktualisiert!")) {
          this.alertService.info("Änderungen wurden erfolgreich gespeichert");
          this.getAllUserDataInfo();
        } else {
          console.error('Fehler bei der Anfrage: Ungültige Antwort');
        }
      },
      error => {
        console.error('Fehler bei der Anfrage:', error);
        this.alertService.warn("Beim Speichern der Änderungen ist ein Fehler aufgetreten")
      }
    );
  }
}

  getAllUserDataInfo() {
    this.AdminService.getDocument().subscribe(response => {
      this.documents = response.documents;
      console.log(this.documents);
    }, error => {
      console.error('lies dir den Text in dieser Meldung! Da stekt die richtige Antwort drin', error);
    });
  }

  deleteDocuments(id: any) {
    const isConfirmed = window.confirm("Möchten Sie dieses Dokument unwiderruflich löschen?")

    if (isConfirmed) {
      this.AdminService.deleteDocuments(id).subscribe(
        response => {
          if (response.includes("Das Dokument wurde erfolgreich gelöscht")) {
            this.alertService.info("Das Dokument wurde erfolgreich gelöscht");
            this.getAllUserDataInfo();
          } else {
            console.error('Fehler bei der Anfrage: Ungültige Antwort');
          }
        },
        error => {
          console.error('Fehler bei der Anfrage:', error);
          this.alertService.warn("Ein Fehler ist beim löschen aufgetreten")
        }
      );
    }
  }

  onFileSelected(event: any): void {

    //ich kann das für mehere Files Anpassen! in dem Fall sollte ich dann unten für jedes Dokument das FormData überschreiben und sooft den Post machen bis es keine 
    //Docs mehr gibt
    this.selectedFile = event.target.files[0] as File;
  }

  //opens data without edit permission
  showDocument(document: any) {
    if(document.id != this.selectedId || !this.isFileSelected) {
      this.isFileSelected = true;
      this.selectEdit = false;
      this.selectedId = document.id;
      this.setFormGroup(document);
      this.dokumentDaten.disable()
    } else if(document.id == this.selectedId && this.isFileSelected && this.selectEdit) {
      this.dokumentDaten.disable();
      this.selectEdit = false;
    } else {
      this.isFileSelected = false;
    }
  }

  //opens data with edit permission
  editDocument(document: any) {
    if(document.id != this.selectedId || !this.isFileSelected) {
      this.isFileSelected = true;
      this.selectedId = document.id;
      this.selectEdit = true;
      this.dokumentDaten.enable();
      this.setFormGroup(document);
    } else if(document.id == this.selectedId && this.isFileSelected && !this.selectEdit) {
      this.dokumentDaten.enable();
      this.selectEdit = true;
    } else {
      this.isFileSelected = false;
      this.selectEdit = false;
    }
  }

  setFormGroup(document:any){
    this.dokumentDaten.patchValue({
      institution: document.institution,
      modul: document.modul,
      description: document.description,
      document: [null]
    });
  }
}
