package com.yazmuh.service;

import com.yazmuh.model.User;
import com.yazmuh.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public User registerUser(User user) {
        // Şimdilik sadece kaydediyoruz.
        // İleride buraya şifre ve email kontrolü eklenecek.
        return userRepository.save(user);
    }
}
