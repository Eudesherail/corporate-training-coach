package com.stubu.studybuddy.api.current_status;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CurrentStatusService {

    private final CurrentStatusRepository currentStatusRepository;

    @Autowired
    public CurrentStatusService(CurrentStatusRepository currentStatusRepository) {
        this.currentStatusRepository = currentStatusRepository;
    }

    public CurrentStatus getCurrentStatus(Long userId, Long topicId) {
        // Optional wird verwendet, um Nullpointer zu vermeiden
        return currentStatusRepository.findByUserIdAndTopicId(userId, topicId)
                .orElse(null); 
    }

    public CurrentStatus getCurrentStatusByUserId(Long userId) {
        return currentStatusRepository.findByUserId(userId)
                .orElse(null);
    }

    public CurrentStatus updateOrCreateCurrentStatus(CurrentStatusDTO currentStatusDTO) {
        // Überprüfung, ob ein Eintrag für die UserID existiert
        Optional<CurrentStatus> statusOptional = currentStatusRepository.findByUserId(
                currentStatusDTO.getUserId());

        CurrentStatus currentStatus;

        if (statusOptional.isPresent()) {
            // Aktualisieren des bestehenden Status
            currentStatus = statusOptional.get();
            currentStatus.setQuestionId(currentStatusDTO.getQuestionId());
            currentStatus.setTopicId(currentStatusDTO.getTopicId());
        } else {
            // Erstellen eines neuen Status
            currentStatus = CurrentStatus.builder()
                    .userId(currentStatusDTO.getUserId())
                    .topicId(currentStatusDTO.getTopicId())
                    .questionId(currentStatusDTO.getQuestionId())
                    .build();
        }

        // Speichern des Status, ob neu oder aktualisiert
        return currentStatusRepository.save(currentStatus);
    }

}