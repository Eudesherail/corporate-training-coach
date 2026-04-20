package com.stubu.studybuddy.api.auth;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*", allowedHeaders = "*")
@RequiredArgsConstructor
public class AuthenticationController {

    private final AuthenticationService authService;

    @PostMapping("/signup")
    public ResponseEntity<AuthenticationResponse> signup(@RequestBody RegisterRequest request) {
        return ResponseEntity.ok(authService.signup(request));
    }

    @PostMapping("/signin")
    public ResponseEntity<AuthenticationResponse> signin(@RequestBody AuthenticationRequest request) {
        return ResponseEntity.ok(authService.signin(request));
    }

    @PostMapping("/oauth2/github")
    public ResponseEntity<AuthenticationResponse> authenticateWithGithub(@RequestBody GithubTokenRequest tokenRequest) {
        System.out.println("url funktioniert");
        return ResponseEntity.ok(authService.authenticateUsingGithub(tokenRequest.getCode()));
    }

    @PostMapping("/oauth2/inviteee")
    public ResponseEntity<AuthenticationResponse> authenticateWithInvite(@RequestBody InviteTokenRequest tokenRequest) {
        System.out.println("url funktioniert");
        return ResponseEntity.ok(authService.authenticateUsingInvite(tokenRequest.getCode()));
    }
}
