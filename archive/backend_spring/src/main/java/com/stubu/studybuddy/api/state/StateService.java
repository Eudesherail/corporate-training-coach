package com.stubu.studybuddy.api.state;

import com.stubu.studybuddy.api.bot.Bot;
import com.stubu.studybuddy.api.user.AppUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

import com.stubu.studybuddy.api.user.AppUserRepo;
import com.stubu.studybuddy.api.bot.BotRepository; // Ich nehme an, dass dieses Repository als BotRepository benannt ist, ändern Sie es entsprechend, wenn der Name anders ist.

@Service
public class StateService {

    private final StateRepository stateRepository;
    private final AppUserRepo appUserRepo; // Hier wurde es geändert
    private final BotRepository botRepository;

    @Autowired
    public StateService(StateRepository stateRepository, AppUserRepo appUserRepo, BotRepository botRepository) {
        this.stateRepository = stateRepository;
        this.appUserRepo = appUserRepo;
        this.botRepository = botRepository;
    }


    public Optional<State> getStateByUserAndBot(Long userId, Long botId) {
        return stateRepository.findByUserIdAndBotId(userId, botId);
    }

    public State saveState(State state, Long userId, Long botId) {
        AppUser user = appUserRepo.findById(userId).orElseThrow(() -> new RuntimeException("User not found"));
        Bot bot = botRepository.findById(botId).orElseThrow(() -> new RuntimeException("Bot not found"));

        state.setUser(user);
        state.setBot(bot);

        return stateRepository.save(state);
    }

    public State setState(Long userId, Long botId, State state) {
        Optional<State> existingStateOpt = getStateByUserAndBot(userId, botId);
        if (existingStateOpt.isPresent()) {
            State existingState = existingStateOpt.get();
            existingState.setCurrentState(state.getCurrentState()); // Ändere nur den State, behalte andere Informationen bei
            return stateRepository.save(existingState);
        } else {
            // Falls es keinen existierenden State gibt, erstelle einen neuen Eintrag
            return saveState(state, userId, botId);
        }
    }
}

