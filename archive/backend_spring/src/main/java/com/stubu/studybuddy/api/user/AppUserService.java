package com.stubu.studybuddy.api.user;

import com.stubu.studybuddy.api.bot.Bot;
import com.stubu.studybuddy.api.bot.BotRepository;
import com.stubu.studybuddy.api.config.AppUserUpdateData;
import com.stubu.studybuddy.security.config.JwtService;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class AppUserService implements UserDetailsService {
    private final AppUserRepo appUserRepo;
    private final JwtService jwtService;
    @Autowired
    private BotRepository botRepository;

    public AppUser updateUserInfo(final UpdateUserInfoRequest request) {
        AppUser user = appUserRepo.findById(request.getUserId()).orElseThrow();
        user.setGoal(request.getGoal());
        user.setTelegramId(request.getTelegramId());
        appUserRepo.save(user);
        return user;
    }

    @Override
    public UserDetails loadUserByUsername(final String email) throws UsernameNotFoundException { // Actually findByEmail
        return appUserRepo.findByEmail(email).orElseThrow(() -> new UsernameNotFoundException("User with email " + email + " not found"));
    }

    public AppUser getAppUserById(Long id) {
        return appUserRepo.findById(id)
            .orElseThrow(() -> new RuntimeException("User not found with id: " + id));
    }
    public Bot getBotByUserId(Long userId) {
        AppUser user = appUserRepo.findById(userId).orElseThrow(() -> new RuntimeException("User not found"));
        System.out.println("User: " + user);  // Logging
        System.out.println("Bot: " + user.getBot());  // Logging
        return user.getBot();
    }
    public AppUser assignBotToUser(Long userId, Long botId) {
        AppUser user = appUserRepo.findById(userId).orElseThrow(() -> new RuntimeException("User not found"));
        Bot bot = botRepository.findById(botId).orElseThrow(() -> new RuntimeException("Bot not found"));
        user.setBot(bot);
        return appUserRepo.save(user);
    }

    public AppUserUpdateData updateUserConfig(final AppUserUpdateData data, final AppUser appUser) {
        if (data.getUsername() != null && !data.getUsername().isEmpty() && !data.getUsername().equals(appUser.getUsername()))
            appUser.setUsername(data.getUsername());
        if (data.getAvatarname() != null && !data.getAvatarname().isEmpty() && !data.getAvatarname().equals(appUser.getAvatarName()))
            appUser.setAvatarName(data.getAvatarname());
        this.appUserRepo.save(appUser);
        data.setAvatarname(appUser.getAvatarName());
        data.setUsername(appUser.getUsername());
        data.setToken(this.jwtService.generateToken(this.loadUserByUsername(appUser.getEmail())));
        return data;
    }
}
