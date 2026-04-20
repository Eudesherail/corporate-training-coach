package com.stubu.studybuddy.api.Admin;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;


@Controller
@CrossOrigin(origins = "*", allowedHeaders = "*")
public class AdminController {

  @Autowired
  private AdminService dateiService;

  @PostMapping("/api/Admin/upload")
  public ResponseEntity<?> ladeMichImVerzeichnis(
    @RequestParam("institution") String institution,
    @RequestParam("modul") String modul,
    @RequestParam("description") String description,
    @RequestParam("document") MultipartFile document,
    @RequestParam("UserID") long UserID)
    throws java.io.IOException {
      String ladeDocument = dateiService.ladeMichImVerzeichnis(institution,modul,description,document,UserID);

      return ResponseEntity.status(HttpStatus.OK)
      .body(ladeDocument);
    
    }
    @PostMapping("/api/Admin/edit")
    public ResponseEntity<?> ändereMich(
    @RequestParam("institution") String institution,
    @RequestParam("modul") String modul,
    @RequestParam("description") String description,
    @RequestParam("document") Optional<MultipartFile> document,
    @RequestParam(value = "userId", required = false) Long userId,
    @RequestParam(value = "id", required = false) Long id)
    throws java.io.IOException {
      String changeDocument = dateiService.ändereMich(institution,modul,description,document,id);
      
      return ResponseEntity.status(HttpStatus.OK)
      .body(changeDocument);
    
    }
 
    @GetMapping("/api/Admin/laden/{userId}")
    public ResponseEntity<AdminDataModell[]> dokumentDownloaden(@PathVariable long userId) {
        AdminDataModell adminData[] = this.dateiService.findByUserId(userId).orElseThrow();
    
        return ResponseEntity.status(HttpStatus.OK)
                .body(adminData);
    }

   @DeleteMapping("/api/Admin/loeschen/{id}")
    public ResponseEntity<?> löscheDatei(@PathVariable long id) throws java.io.IOException {
        String response = dateiService.löscheDokumentMitId(id);
    
        return ResponseEntity.status(HttpStatus.OK)
                .body(response);
    }
    

}
