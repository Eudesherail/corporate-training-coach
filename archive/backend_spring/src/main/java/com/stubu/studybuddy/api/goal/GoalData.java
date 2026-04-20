package com.stubu.studybuddy.api.goal;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class GoalData {
    String goal;
    LocalDate startDate;
    LocalDate endDate;
}
