package com.stubu.studybuddy.api.current_status;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface CurrentStatusRepository extends JpaRepository<CurrentStatus, Long> {
    Optional<CurrentStatus> findByUserIdAndTopicId(Long userId, Long topicId);
    Optional<CurrentStatus> findByUserId(Long userId);
}
