package com.stubu.studybuddy.api.bot;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class BotService {
    private final BotRepository botRepository;

    @Autowired
    public BotService(BotRepository botRepository) {
        this.botRepository = botRepository;
    }

    public List<Bot> getAllBots() {
        return botRepository.findAll();
    }

    public Optional<Bot> getBotById(Long id) {
        return botRepository.findById(id);
    }

    public Optional<Bot> getBotByName(String name) {
        return botRepository.findByName(name);
    }

    public Bot saveBot(Bot bot) {
        return botRepository.save(bot);
    }

    public void deleteBot(Long id) {
        botRepository.deleteById(id);
    }
}

