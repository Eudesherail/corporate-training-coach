package com.stubu.studybuddy.api.goal;

import com.stubu.studybuddy.api.user.AppUser;
import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface GoalRepository extends JpaRepository<Goal, Long> {
    List<Goal> findByAppUser(AppUser appUser);
}
