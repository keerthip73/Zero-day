package com.zeroguard.ai.service;

import com.zeroguard.ai.dto.AuthDtos.AuthResponse;
import com.zeroguard.ai.dto.AuthDtos.LoginRequest;
import com.zeroguard.ai.dto.AuthDtos.MeResponse;
import com.zeroguard.ai.dto.AuthDtos.RegisterRequest;
import com.zeroguard.ai.entity.Role;
import com.zeroguard.ai.entity.User;
import com.zeroguard.ai.repository.UserRepository;
import com.zeroguard.ai.security.JwtService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    public AuthResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new IllegalArgumentException("Email is already registered");
        }
        User user = new User();
        user.setEmail(request.email().toLowerCase());
        user.setPasswordHash(passwordEncoder.encode(request.password()));
        user.setRole(request.role() == null ? Role.ANALYST : request.role());
        User saved = userRepository.save(user);
        return new AuthResponse(jwtService.createToken(saved), saved.getId(), saved.getEmail(), saved.getRole());
    }

    public AuthResponse login(LoginRequest request) {
        User user = userRepository.findByEmail(request.email().toLowerCase())
                .orElseThrow(() -> new IllegalArgumentException("Invalid email or password"));
        if (!passwordEncoder.matches(request.password(), user.getPasswordHash())) {
            throw new IllegalArgumentException("Invalid email or password");
        }
        return new AuthResponse(jwtService.createToken(user), user.getId(), user.getEmail(), user.getRole());
    }

    public MeResponse me(String email) {
        User user = userRepository.findByEmail(email).orElseThrow();
        return new MeResponse(user.getId(), user.getEmail(), user.getRole());
    }
}

