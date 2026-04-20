package com.stubu.studybuddy.api.Admin;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.stubu.studybuddy.api.user.AppUser;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Optional;

@Service
public class AdminService {
    @Autowired
    private AdminDataRepo adminDataRepo;

    private final String FOLDER_PATH ="C:\\Users\\User\\OneDrive\\Bureau\\StudyBuddy3\\StudyBuddy\\backend\\src\\main\\java\\com\\stubu\\studybuddy\\api\\Admin\\documents\\";
    
    public String informiertFastApi(String filename) throws UnsupportedEncodingException {
        HttpClient httpClient = HttpClient.newHttpClient();
        HttpRequest request = null; // Variable außerhalb des try-Blocks deklarieren
    
        String encodedFilename = URLEncoder.encode(filename, StandardCharsets.UTF_8);
        String url = "http://localhost:8000/vektore/" + encodedFilename;
        String requestBody = ""; // Leerer Anfragekörper, da der Dateiname jetzt Teil der URL ist
        request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();
    
        if (request == null) {
            // Wenn ein Fehler beim Erstellen der Anfrage auftritt, gib eine Fehlermeldung zurück
            return "Fehler beim Erstellen der Anfrage.";
        }
    
        try {
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() == 200) {
                return "POST-Anfrage erfolgreich an die FastAPI gesendet.";
            } else {
                return "Fehler beim Senden der POST-Anfrage an die FastAPI. Statuscode: " + response.statusCode();
            }
        } catch (IOException | InterruptedException e) {
            return "Fehler beim Senden der POST-Anfrage: " + e.getMessage();
        }
    }
    public String ladeMichImVerzeichnis(String institution, String modul, String description, MultipartFile file, long userId) {
        String filePath = FOLDER_PATH + file.getOriginalFilename();
        try {

            File fileCkeck = new File(filePath);

            if (fileCkeck.exists()) {
                return "Die Datei existiert bereits.";
            } else {
                AdminDataModell fileData = adminDataRepo.save(
                    AdminDataModell.builder()
                            .name(file.getOriginalFilename())
                            .type(file.getContentType())
                            .filePath(filePath)
                            .description(description)
                            .modul(modul)
                            .institution(institution)
                            .userId(userId)
                            .build()
            );
            file.transferTo(new File(filePath));

            if (fileData != null) {
                String nameCheck = file.getOriginalFilename();
                new Thread(() -> {
                    try {
                        System.out.println(informiertFastApi(nameCheck));
                    } catch (Exception e) {
                        System.err.println("Es gab ein Problem beim Aufrufen von informiertFastApi: " + e.getMessage());
                    }
                }).start();
                return "Das Dokument wurde erfolgreich Hochgeladen :";
            } 
            }

        
        } 
        catch (Exception e) {
            return "Es gab einen Fehler beim laden der Datei";
        }

        return "Fehler";
    }
    //Zum ändern der Infos
     public String ändereMich(String institution, String modul, String description,  Optional<MultipartFile> file,long id) throws IOException {
        Optional<AdminDataModell> documentOptional = adminDataRepo.findById(id);
        if (documentOptional.isPresent()) {
            // Aktualisieren Sie die Eigenschaften des AdminDataModells
            AdminDataModell existingDocument = documentOptional.get();
            existingDocument.setInstitution(institution);
            existingDocument.setModul(modul);
            existingDocument.setDescription(description);

            
            adminDataRepo.save(existingDocument);

            
            return "Erfolgreich aktualisiert!";
        } else {
           
            return "Dokument mit ID " + id + " nicht gefunden.";
        }
    }

    public Optional<AdminDataModell []> findByUserId(long userId) {
        return adminDataRepo.findByUserId(userId);
    }

    public Optional<AdminDataModell> findById(long id) {
        return adminDataRepo.findById(id);
    }

    public String löscheDokumentMitId(long id) {

    Optional<AdminDataModell> documentOptional = adminDataRepo.findById(id);
    if (documentOptional.isPresent()) {
        AdminDataModell document = documentOptional.get();
        String filePath = document.getFilePath();

        try {

            Files.deleteIfExists(Paths.get(filePath));

            adminDataRepo.deleteById(id);
            return "Das Dukument wurde erfolgreich gelöscht";
            
        } catch (Exception e) {
            e.printStackTrace();
            return "Es ist eine Fehler beim löschen der Datei aufgetreten";
        }
            
    }
     return "Das Dukument wurde nicht in der DatenBank gefunden! Das heißt, sie ist entweder nicht mehr referenziert oder sie wurde schon gelöscht";
}


}
