package com.stubu.studybuddy.api.goal;

import com.stubu.studybuddy.api.user.AppUser;
import com.stubu.studybuddy.api.user.AppUserService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class GoalService {

    private final GoalRepository goalRepository;
    private final AppUserService appUserService;

    public List<Goal> getAllGoalsByUserId(Long userId) {
        AppUser appUser = appUserService.getAppUserById(userId);
        return goalRepository.findByAppUser(appUser);
    }

    public Optional<Goal> getGoalById(Long id) {
        return goalRepository.findById(id);
    }

    public Goal saveGoal(Goal goal, Long userId) {
        AppUser appUser = appUserService.getAppUserById(userId);
        goal.setAppUser(appUser);
        return goalRepository.save(goal);
    }

    public Goal updateGoal(Goal goal) {
        return goalRepository.save(goal);
    }

    public void deleteGoal(Long id) {
        goalRepository.deleteById(id);
    }
}
