package com.stubu.studybuddy.api.Admin;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface AdminDataRepo extends JpaRepository<AdminDataModell, Long> {
    Optional<AdminDataModell[]> findByUserId(long userId);
    Optional<AdminDataModell> findById(long id);
    void deleteById(long id);
}