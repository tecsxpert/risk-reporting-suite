package com.internship.tool.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import org.springframework.web.bind.annotation.*;

@RestController
public class AuthController {

    @GetMapping("/auth/test")
    @Operation(summary = "Test API")
    @ApiResponse(responseCode = "200", description = "Success")
    public String test() {
        return "OK";
    }
}