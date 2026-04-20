package com.stubu.studybuddy.api.current_status;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/current_status")
public class CurrentStatusController {

    private final CurrentStatusService currentStatusService;

    @Autowired
    public CurrentStatusController(CurrentStatusService currentStatusService) {
        this.currentStatusService = currentStatusService;
    }

    @GetMapping
    public ResponseEntity<CurrentStatus> getCurrentStatus(@RequestParam Long userId) {
        CurrentStatus currentStatus = currentStatusService.getCurrentStatusByUserId(userId);
        return ResponseEntity.ok(currentStatus);
    }

    @PostMapping
    public ResponseEntity<CurrentStatus> updateOrCreateCurrentStatus(@RequestBody CurrentStatusDTO currentStatusDTO) {
        CurrentStatus updatedStatus = currentStatusService.updateOrCreateCurrentStatus(currentStatusDTO);
        return ResponseEntity.ok(updatedStatus);
    }
}