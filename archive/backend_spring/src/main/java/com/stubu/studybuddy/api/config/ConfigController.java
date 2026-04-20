package com.stubu.studybuddy.api.config;

import com.stubu.studybuddy.api.user.AppUser;
import com.stubu.studybuddy.api.user.AppUserRepo;
import com.stubu.studybuddy.api.user.AppUserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/config")
@RequiredArgsConstructor
public class ConfigController {

    private final AppUserService appUserService;
    private final AppUserRepo appUserRepo;

    @PutMapping("/{id}")
    public ResponseEntity<AppUserUpdateData> updateUser(@PathVariable Long id, @RequestBody AppUserUpdateData data) {
        AppUser appUser = this.appUserRepo.findById(id).orElseThrow();
        AppUserUpdateData returnData = this.appUserService.updateUserConfig(data, appUser);
        return ResponseEntity.ok(returnData);
    }
}
