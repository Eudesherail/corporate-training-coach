package com.stubu.studybuddy.api.current_status;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class CurrentStatusDTO {
    private Long userId;
    private Long topicId;
    private Long questionId;

}