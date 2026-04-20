package com.stubu.studybuddy.api.user;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.stubu.studybuddy.api.bot.Bot;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/user")
@CrossOrigin(origins = "*", allowedHeaders = "*")
@RequiredArgsConstructor
public class AppUserController {

    private final AppUserService appUserService;
    @Autowired
    private ObjectMapper objectMapper;

    @GetMapping("/{userId}/bot")
    public ResponseEntity<String> getBotByUserId(@PathVariable Long userId) {
        Bot bot = appUserService.getBotByUserId(userId);

        // If no bot is assigned, assign the bot with ID 0 and fetch its details
        if (bot == null) {
            ResponseEntity<AppUser> updatedUserResponse = assignBotToUser(userId, 0L);
            if (updatedUserResponse.getStatusCode() != HttpStatus.OK || updatedUserResponse.getBody() == null) {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to assign default bot");
            }
            bot = updatedUserResponse.getBody().getBot();
            if (bot == null) {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to retrieve default bot");
            }
        }

        try {
            String botJson = objectMapper.writeValueAsString(bot);
            System.out.println("Serialized Bot: " + botJson);
            return ResponseEntity.ok(botJson);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Serialization error");
        }
    }


    @PutMapping("/{userId}/bot/{botId}")
    public ResponseEntity<AppUser> assignBotToUser(@PathVariable Long userId, @PathVariable Long botId) {
        AppUser updatedUser = appUserService.assignBotToUser(userId, botId);
        return ResponseEntity.ok(updatedUser);
    }

    @PutMapping("/update")
    public ResponseEntity<AppUser> updateUserInfo(@RequestBody UpdateUserInfoRequest request) {
        return ResponseEntity.ok(appUserService.updateUserInfo(request));
    }
}