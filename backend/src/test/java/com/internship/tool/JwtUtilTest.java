package com.internship.tool;

import com.internship.tool.config.JwtUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class JwtUtilTest {

    @Autowired
    private JwtUtil jwtUtil;

    @Test
    public void testGenerateToken() {
        String token = jwtUtil.generateToken("admin", "ADMIN");
        assertNotNull(token);
    }

    @Test
    public void testExtractUsername() {
        String token = jwtUtil.generateToken("admin", "ADMIN");
        String username = jwtUtil.extractUsername(token);
        assertEquals("admin", username);
    }

    @Test
    public void testValidateToken() {
        String token = jwtUtil.generateToken("admin", "ADMIN");
        assertTrue(jwtUtil.validateToken(token));
    }

    @Test
    public void testInvalidToken() {
        assertFalse(jwtUtil.validateToken("invalid.token.here"));
    }

    @Test
    public void testDifferentRoles() {
        String adminToken = jwtUtil.generateToken("admin", "ADMIN");
        String viewerToken = jwtUtil.generateToken("viewer", "VIEWER");
        assertNotEquals(adminToken, viewerToken);
    }
}
