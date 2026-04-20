package com.stubu.studybuddy.api.state;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/states")
public class StateController {

    private final StateService stateService;

    @Autowired
    public StateController(StateService stateService) {
        this.stateService = stateService;
    }

    @GetMapping
    public State getStateByUserAndBot(@RequestParam Long userId, @RequestParam Long botId) {
        return stateService.getStateByUserAndBot(userId, botId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "State not found"));
    }

    @PostMapping
    public State saveState(@RequestParam Long userId, @RequestParam Long botId, @RequestBody State state) {
        return stateService.saveState(state, userId, botId);
    }

    @PutMapping
    public State setState(@RequestParam Long userId, @RequestParam Long botId, @RequestBody State state) {
        return stateService.setState(userId, botId, state);
    }
}

