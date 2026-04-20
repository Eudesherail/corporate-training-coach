package com.stubu.studybuddy.api.state;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface StateRepository extends JpaRepository<State, Long> {
    @Query("SELECT s FROM State s WHERE s.user.id = :userId AND s.bot.botId = :botId")
    Optional<State> findByUserIdAndBotId(@Param("userId") Long userId, @Param("botId") Long botId);
}

