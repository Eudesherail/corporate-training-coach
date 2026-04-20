package com.stubu.studybuddy;

import com.stubu.studybuddy.api.goal.GoalRepository;
import com.stubu.studybuddy.api.user.AppUserRepo;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class BootstrapCommandLineRunner implements CommandLineRunner {
    private final PasswordEncoder passwordEncoder;
    private final GoalRepository goalRepository;
    private final AppUserRepo appUserRepository;

    @Override
    public void run(final String... args) {
        System.out.println("[BOOTSTRAP] Starting BootstrapCommandLineRunner...");
//        // Delete all existing data
//        goalRepository.deleteAll();
//        appUserRepository.deleteAll();
//
//        // Set up User
//        AppUser user1 = AppUser.builder()
//            .username("Jan")
//            .email("jan.lange@akad.de")
//            .password(passwordEncoder.encode("password"))
//            .appUserRole(AppUserRole.USER)
//            .enabled(true)
//            .locked(false)
//            .build();
//        this.appUserRepository.save(user1);
//        System.out.println("[BOOTSTRAP] User 1 created");
//
//        final AppUser user2 = AppUser.builder()
//            .username("TestUser")
//            .email("test.user@akad.de")
//            .password(passwordEncoder.encode("test"))
//            .appUserRole(AppUserRole.USER)
//            .enabled(true)
//            .locked(false)
//            .build();
//        this.appUserRepository.save(user2);
//        System.out.println("[BOOTSTRAP] User 2 created");
//
//        // Set up Goals
//        final Goal goal1 = Goal
//            .builder()
//            .goal("Ich möchte den verpassten Klausurstoff in Mathe nachholen")
//            .appUser(user1)
//            .startDate(LocalDate.now())
//            .endDate(LocalDate.now().plusDays(28))
//            .build();
//        goalRepository.save(goal1);
//        System.out.println("[BOOTSTRAP] Goal 1 created");
//
//        final Goal goal2 = Goal
//            .builder()
//            .goal("Mich in Deutsch auf eine stabile 1 verbessern.")
//            .appUser(user2)
//            .startDate(LocalDate.now())
//            .endDate(LocalDate.now().plusDays(2))
//            .build();
//        goalRepository.save(goal2);
//        System.out.println("[BOOTSTRAP] Goal 2 created");
    }
}
