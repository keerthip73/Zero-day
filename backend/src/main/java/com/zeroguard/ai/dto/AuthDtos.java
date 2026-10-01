package com.zeroguard.ai.dto;

import com.zeroguard.ai.entity.Role;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.util.UUID;

public class AuthDtos {
    public record RegisterRequest(@Email String email, @Size(min = 8) String password, Role role) {}
    public record LoginRequest(@Email String email, @NotBlank String password) {}
    public record AuthResponse(String token, UUID userId, String email, Role role) {}
    public record MeResponse(UUID userId, String email, Role role) {}
}

