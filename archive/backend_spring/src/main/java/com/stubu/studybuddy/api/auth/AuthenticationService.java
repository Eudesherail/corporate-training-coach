package com.stubu.studybuddy.api.auth;

import com.stubu.studybuddy.api.user.AppUser;
import com.stubu.studybuddy.api.user.AppUserRepo;
import com.stubu.studybuddy.api.user.AppUserRole;
import com.stubu.studybuddy.exceptions.BadRequestException;
import com.stubu.studybuddy.security.config.JwtService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import com.auth0.jwt.JWT;
import com.auth0.jwt.interfaces.DecodedJWT;

import java.util.*;

@Service
@RequiredArgsConstructor
public class AuthenticationService {
    private final AppUserRepo appUserRepo;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authManager;
    @Value("${spring.security.oauth2.client.registration.github.client-id}")
    private String githubClientId;
    @Value("${spring.security.oauth2.client.registration.github.client-secret}")
    private String githubClientSecret;
    @Value("${spring.security.oauth2.client.registration.invite.client-id}")
    private String inviteClientId;
    @Value("${spring.security.oauth2.client.registration.invite.client-secret}")
    private String inviteClientSecret;

    public AuthenticationResponse signup(final RegisterRequest request) {
        // Überprüfung, ob der Benutzername bereits existiert
        if (appUserRepo.existsByUsername(request.getUsername())) {
            throw new BadRequestException("Benutzername bereits vergeben");
        }

        // Überprüfung, ob die E-Mail bereits existiert
        if (appUserRepo.existsByEmail(request.getEmail())) {
            throw new BadRequestException("E-Mail-Adresse bereits registriert");
        }
        AppUser user = AppUser.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .appUserRole(AppUserRole.USER)
                .enabled(true) // TODO - email verification
                .locked(false)
                .build();
        appUserRepo.save(user);
        String jwtToken = jwtService.generateToken(user);
        return AuthenticationResponse.builder().token(jwtToken).userId(user.getId()).username(user.getUsername()).build();
    }

    public AuthenticationResponse signin(final AuthenticationRequest request) {
        Optional<AppUser> optionalUser = appUserRepo.findByEmail(request.getEmail());

        if (!optionalUser.isPresent()) {
            throw new BadRequestException("E-Mail-Adresse nicht gefunden");
        }

        AppUser user = optionalUser.get();

        try {
            authManager.authenticate(new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword()));
        } catch (AuthenticationException e) {
            throw new BadRequestException("Passwort falsch");
        }

        String jwtToken = jwtService.generateToken(user);
        return AuthenticationResponse.builder().token(jwtToken).userId(user.getId()).username(user.getUsername()).build();
    }


    public AuthenticationResponse authenticateUsingGithub(String githubCode) {
        System.out.println("service funktioniert");
        String accessToken = getGithubAccessToken(githubCode);
        System.out.println("gh token funktioniert: " + accessToken);
        String email = getUserEmailFromGithub(accessToken);
        System.out.println("mail funktioniert: " + email);
        String username = email.split("@")[0];
        AppUser user = appUserRepo.findByEmail(email).orElseGet(() -> {
            AppUser newUser = AppUser.builder()
                    .email(email)
                    .username(username)
                    .appUserRole(AppUserRole.USER)
                    .enabled(true)
                    .locked(false)
                    .build();
            return appUserRepo.save(newUser);
        });

        String jwtToken = jwtService.generateToken(user);
        System.out.println("token funktioniert " + jwtToken);
        return AuthenticationResponse.builder().token(jwtToken).userId(user.getId()).username(user.getUsername()).build();
    }

    private String getGithubAccessToken(String code) {
        RestTemplate restTemplate = new RestTemplate();
        String url = "https://github.com/login/oauth/access_token";

        MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
        map.add("client_id", githubClientId);
        map.add("client_secret", githubClientSecret);
        map.add("code", code);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", "application/json");

        ResponseEntity<Map<String, String>> response = restTemplate.exchange(url, HttpMethod.POST, new HttpEntity<>(map, headers), new ParameterizedTypeReference<Map<String, String>>() {});
        return response.getBody().get("access_token");
    }

    private String getUserEmailFromGithub(String accessToken) {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + accessToken);
        headers.set("Accept", "application/json");

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<List<Map<String, Object>>> response = restTemplate.exchange(
                "https://api.github.com/user/emails",
                HttpMethod.GET,
                new HttpEntity<>(headers),
                new ParameterizedTypeReference<List<Map<String, Object>>>() {}
        );

        List<Map<String, Object>> emails = response.getBody();
        if (emails != null && !emails.isEmpty()) {
            for (Map<String, Object> email : emails) {
                if (Boolean.TRUE.equals(email.get("primary")) && Boolean.TRUE.equals(email.get("verified"))) {
                    return (String) email.get("email");
                }
            }
        }
        throw new RuntimeException("No verified primary email found for the user.");
    }

    public AuthenticationResponse authenticateUsingInvite(String inviteCode) {
        String accessToken = getInviteAccessToken(inviteCode);
        // Decode the token
        DecodedJWT jwt;
        try {
            jwt = JWT.decode(accessToken);
        } catch (Exception e) {
            // Handle the exception, maybe throw a custom one or log the error
            throw new RuntimeException("Failed to decode the access token.", e);
        }

        String email = jwt.getClaim("email").asString();
        String givenName = jwt.getClaim("given_name").asString();
        String familyName = jwt.getClaim("family_name").asString();

        AppUser user = appUserRepo.findByEmail(email).orElseGet(() -> {
            AppUser newUser = AppUser.builder()
                    .email(email)
                    .username(givenName + " " + familyName)
                    .appUserRole(AppUserRole.USER)
                    .enabled(true)
                    .locked(false)
                    .build();
            return appUserRepo.save(newUser);
        });

        String jwtToken = jwtService.generateToken(user);
        return AuthenticationResponse.builder().token(jwtToken).userId(user.getId()).username(user.getUsername()).build();
    }


    private String getInviteAccessToken(String code) {
        RestTemplate restTemplate = new RestTemplate();
        String url = "https://auth-preview.invite-toolcheck.de/oauth2/token";

        MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
        map.add("client_id", inviteClientId);
        map.add("client_secret", inviteClientSecret);
        map.add("code", code);
        map.add("grant_type", "authorization_code");
        map.add("redirect_uri", "https://stubu.oks.de/auth-callback");  // Add this line


        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", "application/json");

        ResponseEntity<Map<String, String>> response = restTemplate.exchange(url, HttpMethod.POST, new HttpEntity<>(map, headers), new ParameterizedTypeReference<Map<String, String>>() {});
        return response.getBody().get("id_token");
    }

    private Map<String, Object> getUserInfoFromInvite(String accessToken) {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + accessToken);
        headers.set("Accept", "application/json");

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                "https://auth.invite-toolcheck.de/userinfo_endpoint", // Replace 'userinfo_endpoint' with the correct endpoint if this isn't it.
                HttpMethod.GET,
                new HttpEntity<>(headers),
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        return response.getBody();
    }

}
