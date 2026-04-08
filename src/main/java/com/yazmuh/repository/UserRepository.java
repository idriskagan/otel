package com.yazmuh.repository;

import com.yazmuh.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // Login için e-posta ile kullanıcı bulmamız gerekecek
    boolean existsByEmail(String email);
}