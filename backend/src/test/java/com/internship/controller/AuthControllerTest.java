package com.internship.tool.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AuthController.class)
@AutoConfigureMockMvc(addFilters = false)   // ✅ THIS FIXES 401
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void testAPI() throws Exception {
        mockMvc.perform(get("/auth/test"))
                .andExpect(status().isOk());
    }
}