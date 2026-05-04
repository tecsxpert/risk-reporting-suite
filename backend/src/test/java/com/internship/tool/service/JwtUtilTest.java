package com.internship.tool.service;

import com.internship.tool.security.JwtUtil;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class JwtUtilTest {

    @Test
    void testToken() {
        JwtUtil jwt = new JwtUtil();
        String token = jwt.generateToken("user");
        assertNotNull(token);
    }
}