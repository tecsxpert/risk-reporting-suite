package com.internship.tool.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuthController {

    @Autowired
    private JwtUtil jwtUtil;

    @Autowired
    private PasswordEncoder passwordEncoder;

    // POST /auth/register
    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody User user) {
        if (userRepository.existsByUsername(user.getUsername())) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body(Map.of("error", "Username already exists"));
        }
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        if (user.getRole() == null || user.getRole().isEmpty()) { user.setRole("VIEWER"); }
        userRepository.save(user);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(Map.of("message", "User registered successfully"));
    }

    // POST /auth/login
    @PostMapping("/login")
    public Map<String, String> login(@RequestBody Map<String, String> body) {

        String username = body.get("username");
        String password = body.get("password");

        if ("admin".equals(username) && "admin".equals(password)) {
            String token = jwtUtil.generateToken(username);
            return Map.of("token", token);
        }

        throw new RuntimeException("Invalid credentials");
    }
}