package com.stubu.studybuddy.api.bot;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// Vorberitet, aber bisher nur für Role Admin
// TO-DO: Admin im Rest implementieren und SecurityConfig
@RestController
@RequestMapping("/api/bots")
//@PreAuthorize("hasRole('ROLE_ADMIN')")
public class BotController {
    private final BotService botService;

    @Autowired
    public BotController(BotService botService) {
        this.botService = botService;
    }

    @GetMapping
    public List<Bot> getAllBots() {
        return botService.getAllBots();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Bot> getBotById(@PathVariable Long id) {
        return botService.getBotById(id)
                .map(bot -> ResponseEntity.ok(bot))
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public Bot createBot(@RequestBody Bot bot) {
        return botService.saveBot(bot);
    }

    @DeleteMapping("/{id}")
    public void deleteBot(@PathVariable Long id) {
        botService.deleteBot(id);
    }
}
